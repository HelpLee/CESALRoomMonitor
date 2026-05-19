"""
CESAL Room Monitor with Telegram notification - simple no-Python-ready version

This script monitors the CESAL resident housing reservation page with Microsoft Edge
and Selenium. It is intended for low-frequency personal monitoring of your own CESAL
resident account.

It does not bypass login, captcha, authentication, access control, or any security
mechanism. It does not submit a final room reservation automatically.
"""

from __future__ import annotations

import json
import os
import sys
import random
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

HOME_URL = "https://logement.cesal.fr/espace-resident/index.php"
RESERVE_URL = "https://logement.cesal.fr/espace-resident/cesal_mon_logement_reservation.php"
PROJECT_ROOT = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
ENV_FILE = PROJECT_ROOT / ".env"
CONFIG_FILE = PROJECT_ROOT / "config.txt"
LOG_DIR = PROJECT_ROOT / "logs"
STATE_DIR = PROJECT_ROOT / "state"
LOG_FILE = LOG_DIR / "cesal_room_log.txt"
STATE_FILE = STATE_DIR / "cesal_notification_state.json"


def load_key_value_file(path: Path) -> None:
    """Load simple KEY=VALUE pairs from config.txt or .env."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_configuration() -> None:
    """Load user configuration from config.txt first, then optional .env."""
    load_key_value_file(CONFIG_FILE)
    load_key_value_file(ENV_FILE)


def env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or not str(value).strip():
        return default
    return int(str(value).strip())


load_configuration()
def env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or not str(value).strip():
        return default
    return float(str(value).strip())


def get_wait_seconds() -> tuple[int, int]:
    """Return randomized monitoring interval from minute-range settings."""
    min_minutes = env_float("CHECK_INTERVAL_MINUTES_MIN", 6.0)
    max_minutes = env_float("CHECK_INTERVAL_MINUTES_MAX", 12.0)

    min_seconds = max(60, int(min_minutes * 60))
    max_seconds = max(60, int(max_minutes * 60))

    if max_seconds < min_seconds:
        raise ValueError("CHECK_INTERVAL_MINUTES_MAX must be >= CHECK_INTERVAL_MINUTES_MIN.")

    return min_seconds, max_seconds


_WAIT_MIN_SECONDS, _WAIT_MAX_SECONDS = get_wait_seconds()



@dataclass(frozen=True)
class Settings:
    """Runtime configuration loaded from environment variables or .env."""

    profile_dir: str = os.getenv("CESAL_EDGE_PROFILE_DIR", r"C:\cesal_edge_profile")
    end_date: str = os.getenv("CESAL_END_DATE", "31/12/2026")
    page_wait_seconds: int = env_int("CESAL_PAGE_WAIT_SECONDS", 5)
    min_wait_seconds: int = _WAIT_MIN_SECONDS
    max_wait_seconds: int = _WAIT_MAX_SECONDS

    enable_telegram: bool = env_bool("ENABLE_TELEGRAM", True)
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    telegram_auto_discover_chat_id: bool = env_bool("TELEGRAM_AUTO_DISCOVER_CHAT_ID", True)
    telegram_startup_test: bool = env_bool("TELEGRAM_STARTUP_TEST", False)

    send_first_successful_check: bool = env_bool("SEND_FIRST_SUCCESSFUL_CHECK", True)
    notify_only_on_change: bool = env_bool("NOTIFY_ONLY_ON_CHANGE", True)

    headless: bool = env_bool("CESAL_HEADLESS", False)


SETTINGS = Settings()
RESOLVED_TELEGRAM_CHAT_ID: int | str | None = None


class PersistentNotificationState:
    """Small JSON state file used to avoid repeated identical notifications."""

    def __init__(self, path: Path):
        self.path = path
        self.signature: str | None = None
        self.last_notification_ts: float | None = None
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.signature = data.get("signature")
            self.last_notification_ts = data.get("last_notification_ts")
        except Exception:
            self.signature = None
            self.last_notification_ts = None

    def save(self, signature: str) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        now = time.time()
        payload = {
            "signature": signature,
            "last_notification_ts": now,
            "last_notification_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        self.signature = signature
        self.last_notification_ts = now


NOTIFICATION_STATE = PersistentNotificationState(STATE_FILE)


def log(message: str) -> None:
    """Print a timestamped message and append it to logs/cesal_room_log.txt."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {message}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(line + "\n")


def validate_settings() -> None:
    """Validate common configuration mistakes before starting Selenium."""
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", SETTINGS.end_date):
        raise ValueError("CESAL_END_DATE must use dd/mm/yyyy format, for example 31/12/2026.")
    if SETTINGS.min_wait_seconds < 60:
        raise ValueError("CHECK_INTERVAL_MINUTES_MIN is too short. Use at least 1 minute.")
    if SETTINGS.max_wait_seconds < SETTINGS.min_wait_seconds:
        raise ValueError("CHECK_INTERVAL_MINUTES_MAX must be >= CHECK_INTERVAL_MINUTES_MIN.")


def countdown_sleep(seconds: int) -> None:
    """Display a single-line countdown before the next check."""
    for remaining in range(seconds, 0, -1):
        minutes, secs = divmod(remaining, 60)
        print(f"\rNext check in {minutes:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)
    print()


def telegram_config_ready() -> bool:
    """Return True only when Telegram is enabled and the bot token is configured."""
    if not SETTINGS.enable_telegram:
        return False
    token = SETTINGS.telegram_bot_token.strip()
    if not token:
        return False
    placeholder_words = ["your_telegram_bot_token", "your_token", "bot_token", "<token>"]
    if any(word in token.lower() for word in placeholder_words):
        return False
    return ":" in token


def normalize_telegram_chat_id(chat_id: Any) -> int | str | None:
    """Normalize Telegram chat_id; numeric private IDs are sent as int."""
    if chat_id is None:
        return None
    text = str(chat_id).strip().replace("\u200b", "").replace("\ufeff", "")
    if not text:
        return None
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    return text


def telegram_api_request(method: str, payload: dict[str, Any] | None = None, timeout: int = 15):
    """Call Telegram Bot API and return the requests.Response object."""
    token = SETTINGS.telegram_bot_token.strip()
    url = f"https://api.telegram.org/bot{token}/{method}"
    if payload is None:
        return requests.get(url, timeout=timeout)
    return requests.post(url, json=payload, timeout=timeout)


def get_telegram_bot_info() -> dict[str, Any]:
    """Return Telegram bot metadata from getMe, or an empty dict."""
    if not telegram_config_ready():
        return {}
    try:
        response = telegram_api_request("getMe", timeout=10)
        if not response.ok:
            log(f"Telegram getMe failed: HTTP {response.status_code}: {response.text}")
            return {}
        data = response.json()
        if not data.get("ok"):
            log(f"Telegram getMe returned not-ok response: {data}")
            return {}
        return data.get("result", {}) or {}
    except Exception as exc:
        log(f"Telegram getMe failed: {exc}")
        return {}


def discover_telegram_chat_id() -> int | str | None:
    """
    Discover the latest private chat_id from getUpdates.

    Before this can work, open your bot in Telegram, send /start, then send a
    normal message such as test123. If getUpdates is empty, send test123 again
    and rerun this script.
    """
    if not telegram_config_ready():
        return None
    try:
        response = telegram_api_request("getUpdates", timeout=10)
        if not response.ok:
            log(f"Telegram getUpdates failed: HTTP {response.status_code}: {response.text}")
            return None
        data = response.json()
        if not data.get("ok"):
            log(f"Telegram getUpdates returned not-ok response: {data}")
            return None
        updates = data.get("result", []) or []
        if not updates:
            log("Telegram getUpdates returned no messages. Send /start and test123 to your bot, then rerun.")
            return None
        for update in reversed(updates):
            message = update.get("message") or update.get("edited_message") or {}
            chat = message.get("chat") or {}
            chat_id = chat.get("id")
            chat_type = chat.get("type")
            if chat_id is not None and chat_type == "private":
                return normalize_telegram_chat_id(chat_id)
        for update in reversed(updates):
            message = update.get("message") or update.get("edited_message") or {}
            chat = message.get("chat") or {}
            chat_id = chat.get("id")
            if chat_id is not None:
                return normalize_telegram_chat_id(chat_id)
        log("Telegram getUpdates contained updates, but no chat.id was found.")
        return None
    except Exception as exc:
        log(f"Telegram getUpdates failed: {exc}")
        return None


def get_effective_telegram_chat_id() -> int | str | None:
    """Return the chat_id used for Telegram sending."""
    global RESOLVED_TELEGRAM_CHAT_ID
    if RESOLVED_TELEGRAM_CHAT_ID is not None:
        return RESOLVED_TELEGRAM_CHAT_ID
    if SETTINGS.telegram_auto_discover_chat_id:
        discovered = discover_telegram_chat_id()
        if discovered is not None:
            RESOLVED_TELEGRAM_CHAT_ID = discovered
            log(f"Telegram chat id resolved from getUpdates: {RESOLVED_TELEGRAM_CHAT_ID}")
            return RESOLVED_TELEGRAM_CHAT_ID
    return normalize_telegram_chat_id(SETTINGS.telegram_chat_id)


def send_telegram_message(message: str, retry_on_chat_not_found: bool = True) -> bool:
    """Send a Telegram message using Telegram Bot API."""
    global RESOLVED_TELEGRAM_CHAT_ID
    if not SETTINGS.enable_telegram:
        return False
    if not telegram_config_ready():
        log("Telegram configuration is incomplete; skipping Telegram notification.")
        return False
    chat_id = get_effective_telegram_chat_id()
    if chat_id is None:
        log("Telegram chat id is empty; skipping Telegram notification.")
        return False
    if len(message) > 3900:
        message = message[:3800] + "\n\n[Message truncated]"
    payload = {"chat_id": chat_id, "text": message, "disable_web_page_preview": True}
    try:
        response = telegram_api_request("sendMessage", payload=payload, timeout=15)
        if response.ok:
            log("Telegram notification sent.")
            return True
        log(f"Telegram notification failed: HTTP {response.status_code}: {response.text}")
        if retry_on_chat_not_found and "chat not found" in response.text.lower():
            log("Telegram says chat not found. Send test123 to the bot, rediscovering chat_id and retrying once.")
            RESOLVED_TELEGRAM_CHAT_ID = None
            discovered = discover_telegram_chat_id()
            if discovered is not None:
                RESOLVED_TELEGRAM_CHAT_ID = discovered
                return send_telegram_message(message, retry_on_chat_not_found=False)
        return False
    except Exception as exc:
        log(f"Telegram notification failed: {exc}")
        return False


def test_telegram_configuration(send_test_message: bool = False) -> None:
    """Log Telegram diagnostic information at startup."""
    if not SETTINGS.enable_telegram:
        log("Telegram enabled: False")
        return
    log(f"Telegram enabled: True; token configured: {telegram_config_ready()}")
    if not telegram_config_ready():
        log("Set TELEGRAM_BOT_TOKEN in .env before expecting Telegram notifications.")
        return
    bot_info = get_telegram_bot_info()
    if bot_info:
        username = bot_info.get("username", "unknown")
        bot_id = bot_info.get("id", "unknown")
        log(f"Telegram bot detected: @{username} / id={bot_id}")
    effective_chat_id = get_effective_telegram_chat_id()
    log(f"Telegram configured chat id: {SETTINGS.telegram_chat_id or '[empty]'}")
    log(f"Telegram effective chat id: {effective_chat_id}")
    if send_test_message:
        send_telegram_message("Test: CESAL room alert Telegram notification is working.")


def make_result_signature(results: list[dict[str, Any]], arrival_date: str, end_date: str) -> str:
    """Build a stable signature of the meaningful parsed result."""
    normalized = {
        "arrival_date": arrival_date,
        "end_date": end_date,
        "residences": sorted(
            [
                {
                    "residence": str(item.get("residence", "")).strip(),
                    "available": int(item.get("available", 0)),
                    "status": str(item.get("status", "")).strip(),
                }
                for item in results
            ],
            key=lambda item: item["residence"],
        ),
    }
    return json.dumps(normalized, ensure_ascii=False, sort_keys=True)


def should_send_change_notification(signature: str) -> tuple[bool, str]:
    """Decide whether this result should trigger a Telegram notification."""
    previous = NOTIFICATION_STATE.signature
    if previous is None:
        if SETTINGS.send_first_successful_check:
            return True, "first successful check"
        NOTIFICATION_STATE.save(signature)
        return False, "first successful check recorded without notification"
    if not SETTINGS.notify_only_on_change:
        return True, "notification mode allows every successful check"
    if signature != previous:
        return True, "availability result changed"
    return False, "availability result unchanged"


def create_driver():
    options = Options()
    options.add_argument(f"--user-data-dir={SETTINGS.profile_dir}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-session-crashed-bubble")
    options.add_argument("--disable-restore-session-state")
    if SETTINGS.headless:
        options.add_argument("--headless=new")
    options.add_experimental_option("prefs", {"profile.exit_type": "Normal", "profile.exited_cleanly": True})
    return webdriver.Edge(options=options)


def is_login_page(driver) -> bool:
    """Detect whether the browser is currently on the login page."""
    url = driver.current_url.lower()
    if "login" in url or "connexion" in url:
        return True
    has_password_input = len(driver.find_elements(By.XPATH, "//input[@type='password']")) > 0
    has_login_button = any(
        element.is_displayed()
        for element in driver.find_elements(
            By.XPATH,
            "//*[contains(translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'se connecter')]",
        )
    )
    return has_password_input and has_login_button


def parse_french_date(date_text: str) -> datetime:
    """Parse a date in dd/mm/yyyy format."""
    return datetime.strptime(date_text.strip(), "%d/%m/%Y")


def go_to_reservation_page(driver) -> None:
    """Open the resident homepage, wait for manual login if needed, then open reservation page."""
    driver.get(HOME_URL)
    time.sleep(SETTINGS.page_wait_seconds)
    if is_login_page(driver):
        log("Login page detected. Please log in manually in the Edge window.")
        input("After login and after the homepage is visible, press Enter here to continue...")
    driver.get(RESERVE_URL)
    time.sleep(SETTINGS.page_wait_seconds)


def choose_last_arrival_date(driver) -> str:
    """Select the latest available arrival date shown by CESAL."""
    wait = WebDriverWait(driver, 20)
    selects = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "select")))
    target_select = None
    available_dates: list[tuple[str, str | None]] = []
    for select_element in selects:
        try:
            select = Select(select_element)
            date_options = []
            for option in select.options:
                text = option.text.strip()
                value = option.get_attribute("value")
                if re.match(r"^\d{2}/\d{2}/\d{4}$", text):
                    date_options.append((text, value))
            if date_options:
                target_select = select_element
                available_dates = date_options
                break
        except Exception:
            continue
    if target_select is None:
        raise RuntimeError("Arrival-date dropdown was not found. The page structure may have changed.")
    available_dates = sorted(available_dates, key=lambda item: parse_french_date(item[0]))
    chosen_text, chosen_value = available_dates[-1]
    select = Select(target_select)
    if chosen_value:
        select.select_by_value(chosen_value)
    else:
        select.select_by_visible_text(chosen_text)
    driver.execute_script("const el = arguments[0]; el.dispatchEvent(new Event('change', { bubbles: true }));", target_select)
    log(f"Selected arrival date: {chosen_text}")
    time.sleep(2)
    return chosen_text


def fill_end_date(driver, end_date: str) -> None:
    """Fill the desired lease end date field."""
    inputs = driver.find_elements(By.TAG_NAME, "input")
    candidates = []
    for input_element in inputs:
        if input_element.is_displayed() and input_element.is_enabled():
            input_type = (input_element.get_attribute("type") or "").lower()
            name = input_element.get_attribute("name") or ""
            placeholder = input_element.get_attribute("placeholder") or ""
            css_class = input_element.get_attribute("class") or ""
            score = 0
            if input_type in ["text", "date", ""]:
                score += 1
            if "date" in name.lower():
                score += 2
            if "bail" in name.lower():
                score += 3
            if "datepicker" in css_class.lower():
                score += 2
            if "date" in placeholder.lower():
                score += 1
            candidates.append((score, input_element))
    if not candidates:
        raise RuntimeError("Lease end-date input field was not found.")
    candidates.sort(key=lambda item: item[0], reverse=True)
    target_input = candidates[0][1]
    target_input.clear()
    target_input.send_keys(end_date)
    driver.execute_script(
        "const el = arguments[0]; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true }));",
        target_input,
    )
    log(f"Filled lease end date: {end_date}")
    time.sleep(1)


def click_validate(driver) -> None:
    """Click the Valider button and wait for the residence availability page."""
    wait = WebDriverWait(driver, 20)
    button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[self::button or self::input or self::a][contains(normalize-space(), 'Valider') or @value='Valider']")
        )
    )
    button.click()
    log("Clicked Valider. Waiting for the availability list to load.")
    time.sleep(6)
    try:
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(3)
    except NoAlertPresentException:
        pass


def parse_all_residences(page_text: str) -> list[dict[str, Any]]:
    """Parse every residence from the visible text of the result page."""
    lines = [line.strip() for line in page_text.splitlines() if line.strip()]
    results = []
    current_residence = None
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.lower() == "résidence" and index + 1 < len(lines):
            next_line = lines[index + 1]
            if not re.search(r"logement|disponible|aucun", next_line, flags=re.I):
                current_residence = f"Résidence {next_line}"
                index += 2
                continue
        if line.lower().startswith("résidence"):
            current_residence = line
        available_match = re.search(r"(\d+)\s+logements?\s+disponibles?", line, flags=re.I)
        if available_match and current_residence:
            results.append({"residence": current_residence, "available": int(available_match.group(1)), "status": "available"})
            current_residence = None
        if re.search(r"Aucun logement disponible", line, flags=re.I) and current_residence:
            results.append({"residence": current_residence, "available": 0, "status": "none"})
            current_residence = None
        index += 1
    final: dict[str, dict[str, Any]] = {}
    for item in results:
        final[item["residence"]] = item
    return list(final.values())


def compact_residence_name(name: str) -> str:
    """Convert residence names to a short watch-friendly form, e.g. Résidence III -> RIII."""
    text = str(name or "").strip()
    text = re.sub(r"^r[ée]sidence\s*", "", text, flags=re.I).strip()
    text = re.sub(r"\s+", "", text)
    return f"R{text}" if text else "R?"


def format_watch_summary(results: list[dict[str, Any]], total_available: int) -> str:
    """Build a short summary that appears first on watches and lock screens."""
    parts = [f"{compact_residence_name(item.get('residence', ''))}={int(item.get('available', 0))}" for item in sorted(results, key=lambda x: str(x.get("residence", "")))]
    compact = ", ".join(parts) if parts else "no parsed residence"
    return f"CESAL: total {total_available} | {compact}"


def format_report(results: list[dict[str, Any]], arrival_date: str, end_date: str) -> str:
    """Build a plain-text report for terminal and Telegram."""
    lines = [
        "CESAL room availability report",
        f"Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Arrival date: {arrival_date}",
        f"Lease end date: {end_date}",
        "",
    ]
    total = 0
    for item in results:
        total += int(item["available"])
        if int(item["available"]) > 0:
            lines.append(f"{item['residence']}: available, {item['available']} room(s)")
        else:
            lines.append(f"{item['residence']}: not available, 0 room(s)")
    lines.extend(["", f"Total available rooms: {total}", f"Page: {RESERVE_URL}"])
    return "\n".join(lines)


def check_once(driver) -> None:
    """Run one full monitoring cycle."""
    go_to_reservation_page(driver)
    if is_login_page(driver):
        log("Still on the login page. Please log in manually again.")
        input("After login is complete, press Enter here to continue...")
        go_to_reservation_page(driver)
    arrival_date = choose_last_arrival_date(driver)
    fill_end_date(driver, SETTINGS.end_date)
    click_validate(driver)
    page_text = driver.find_element(By.TAG_NAME, "body").text
    results = parse_all_residences(page_text)
    if not results:
        log("No residence information was parsed. The page structure may have changed.")
        return
    log("Check result:")
    for item in results:
        if int(item["available"]) > 0:
            log(f"  {item['residence']}: available, {item['available']} room(s)")
        else:
            log(f"  {item['residence']}: not available, 0 room(s)")
    total_available = sum(int(item["available"]) for item in results)
    if total_available > 0:
        log(f"Available rooms found. Total: {total_available}")
    else:
        log("No rooms are currently available.")
    signature = make_result_signature(results, arrival_date, SETTINGS.end_date)
    should_send, reason = should_send_change_notification(signature)
    if not should_send:
        log(f"Telegram notification skipped: {reason}.")
        return
    watch_summary = format_watch_summary(results, total_available)
    report = format_report(results, arrival_date, SETTINGS.end_date)
    notification_message = (
        f"{watch_summary}\n"
        f"Arrive {arrival_date} -> {SETTINGS.end_date}\n"
        f"{datetime.now().strftime('%m-%d %H:%M')} | {reason}\n\n"
        f"{report}"
    )
    sent = send_telegram_message(notification_message)
    if sent:
        NOTIFICATION_STATE.save(signature)
    else:
        log("Telegram notification was not saved as delivered because sending failed.")


def main() -> None:
    validate_settings()
    log("Starting CESAL room monitor.")
    log(f"Running file: {__file__}")
    log(f"Configured lease end date: {SETTINGS.end_date}")
    log("Arrival-date strategy: automatically select the latest available date shown by the page.")
    test_telegram_configuration(send_test_message=SETTINGS.telegram_startup_test)
    driver = create_driver()
    try:
        while True:
            try:
                check_once(driver)
            except Exception as exc:
                log(f"This check failed: {exc}")
            wait_seconds = random.randint(SETTINGS.min_wait_seconds, SETTINGS.max_wait_seconds)
            log(f"Next check will start in {wait_seconds // 60} min {wait_seconds % 60} sec.")
            countdown_sleep(wait_seconds)
    finally:
        # The browser is intentionally not closed automatically. Keeping it alive
        # helps preserve the CESAL session. Close Edge manually when stopping use.
        pass


if __name__ == "__main__":
    main()
