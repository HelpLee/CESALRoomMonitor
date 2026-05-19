# CESAL Room Monitor

English | [中文说明](#中文说明)

A lightweight Windows portable tool for monitoring the CESAL resident housing reservation page. It opens Microsoft Edge, lets the user log in manually when required, checks residence availability at a low frequency, and sends Telegram notifications when rooms are available or when the availability result changes.

> This project is for personal, low-frequency monitoring of your own CESAL resident account. It does not bypass login, captcha, access control, or any security mechanism. It does not automatically reserve a room.

---

## What this project does

- Opens the CESAL resident area with Microsoft Edge.
- Lets the user log in manually when CESAL requires login.
- Reuses the same browser session during monitoring.
- Opens the CESAL reservation page.
- Automatically selects the latest available arrival date shown by the page.
- Fills in the configured lease end date.
- Clicks `Valider`.
- Reads the availability result for each residence.
- Sends Telegram notifications when availability is found or when the result changes.
- Uses a configurable random check interval, for example 6 to 12 minutes.
- Writes local logs and notification state.

---

## Recommended way to use: Windows portable release

For normal users, the recommended way is to download the Windows portable version from GitHub Releases.

The portable version does not require Python, Anaconda, pip, or manual dependency installation.

You only need:

- Windows
- Microsoft Edge
- Telegram
- A valid CESAL resident account

### Download

Go to:

```text
Releases -> latest version -> Assets
```

Download:

```text
CESALRoomMonitor_Windows_NoPython.zip
```

Extract it to a local folder.

After extraction, you should see files similar to:

```text
CESALRoomMonitor.exe
config.example.txt
README_FIRST_USE.txt
logs/
state/
```

---

## First-time configuration

### Step 1: Create `config.txt`

Copy:

```text
config.example.txt
```

Rename the copied file to:

```text
config.txt
```

Do not edit `config.example.txt` directly. Use `config.txt` for your own private configuration.

### Step 2: Edit the required settings

Open `config.txt` with Notepad or another text editor.

Normally, you only need to edit:

```text
CESAL_END_DATE=19/06/2027
TELEGRAM_BOT_TOKEN=PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE
```

If the default lease end date is already correct, then you only need to fill in `TELEGRAM_BOT_TOKEN`.

### Step 3: Configure the check interval

The default check interval is:

```text
CHECK_INTERVAL_MINUTES_MIN=6
CHECK_INTERVAL_MINUTES_MAX=12
```

This means that after each check, the program randomly waits 6 to 12 minutes before the next check.

You can change it, for example:

```text
CHECK_INTERVAL_MINUTES_MIN=10
CHECK_INTERVAL_MINUTES_MAX=20
```

Do not set the interval too short. A value lower than 5 minutes is not recommended.

---

## How to get a Telegram bot token

1. Open Telegram.
2. Search for `@BotFather`.
3. Open the chat with BotFather.
4. Send:

```text
/newbot
```

5. Follow the instructions.
6. BotFather will ask you to set a display name and a username.
7. The bot username must end with `bot`, for example:

```text
cesal_room_alert_abc_bot
```

8. After the bot is created, BotFather will send you a token similar to:

```text
123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

9. Copy that token into `config.txt`:

```text
TELEGRAM_BOT_TOKEN=123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Important: the Telegram bot token is private. Do not upload `config.txt` to GitHub and do not share your real token.

---

## Wake up the Telegram bot

Before running the program, open your Telegram bot chat and send:

```text
/start
```

Then send:

```text
test123
```

This is necessary because a Telegram bot cannot send messages to you until you have started a chat with it.

It is recommended to send `test123` again before running the monitor each day. This helps the program discover your latest Telegram chat ID automatically.

---

## Run the program

Double-click:

```text
CESALRoomMonitor.exe
```

A black command window will open first. Microsoft Edge will open automatically after the program finishes initialization.

### First run may be slow

The first run may take about 30 seconds to 1 minute before the Edge browser appears. Please wait patiently and do not double-click the program repeatedly.

If several program windows are opened at the same time, close the extra windows and keep only one instance running.

### Manual CESAL login

If CESAL asks you to log in:

1. Go to the opened Microsoft Edge browser.
2. Log in to your CESAL resident account manually.
3. If Edge asks whether to save the password, you may choose to save or remember the password on your own trusted computer.
4. Wait until the CESAL resident homepage or resident area is fully visible.
5. Return to the black command window.
6. Press `Enter` to continue.

### How the program knows login is complete

The program does not read your password and does not automatically submit login credentials.

When it detects the CESAL login page, it pauses and waits for you. After you manually log in, you confirm completion by pressing `Enter` in the black command window. Then the program opens the reservation page again.

If it is still on the login page, the program will ask you to log in again.

### Login time limit

There is no short program-side countdown while the program is waiting at the login prompt. In normal use, you can take several minutes to enter the username, password, and any verification required by CESAL.

However, the CESAL website itself may have its own session timeout or login timeout. If the website expires the login page, refresh or log in again, then return to the command window and press `Enter` after the resident page is visible.

---

## How to stop

In the black command window, press:

```text
Ctrl + C
```

Then confirm if the terminal asks you to stop the program.

---

## Repository structure

```text
CESALRoomMonitor/
├── .github/workflows/              # GitHub Actions workflow for Windows exe build
├── check_cesal_rooms.py            # Main monitoring script
├── config.example.txt              # Public configuration template
├── README.md                       # Repository README
├── README_FIRST_USE.txt            # Detailed first-use guide for release users
├── requirements.txt                # Python dependencies for development/build
├── environment.yml                 # Optional Conda environment file
├── BUILD_EXE_ON_WINDOWS.bat        # Optional local Windows build script
├── LICENSE                         # License file
├── logs/                           # Runtime logs, local only
└── state/                          # Runtime notification state, local only
```

---

## Build the Windows executable with GitHub Actions

This repository includes a GitHub Actions workflow.

1. Push the source code to GitHub.
2. Open the repository page.
3. Go to:

```text
Actions -> Build Windows EXE
```

4. Click:

```text
Run workflow
```

5. Wait until the workflow succeeds.
6. Open the successful workflow run.
7. Download the artifact:

```text
CESALRoomMonitor_Windows_NoPython
```

The artifact is a zip file containing the Windows portable version.

---

## Publish a GitHub Release

After downloading the artifact from GitHub Actions, publish it as a Release so normal users can download it easily.

Recommended flow:

1. Open the repository page.
2. Go to `Releases`.
3. Click `Draft a new release`.
4. Set a tag, for example:

```text
v1.0.0
```

5. Set a release title, for example:

```text
CESAL Room Monitor v1.0.0
```

6. Upload the artifact zip as a release asset.
7. Click `Publish release`.

Normal users should download the program from:

```text
Releases -> latest version -> Assets
```

They do not need to download the source code.

---

## Local development

For developers who want to run the source code directly:

```bash
conda env create -f environment.yml
conda activate cesal_bot
python check_cesal_rooms.py
```

Or with pip:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python check_cesal_rooms.py
```

To build locally on Windows:

```text
BUILD_EXE_ON_WINDOWS.bat
```

For normal users, local development is not required. Use the Release version instead.

---

## Privacy and security

Do not upload these files:

```text
config.txt
.env
logs/*
state/*
```

`config.example.txt` is safe to share because it only contains placeholders.

`config.txt` is private because it contains your real Telegram bot token.

If your Telegram token is accidentally uploaded or shared, revoke it immediately in `@BotFather` and generate a new one.

---

## Troubleshooting

### Telegram token is not configured

If the program says the Telegram token is not configured, check that:

- `config.txt` exists in the same folder as `CESALRoomMonitor.exe`.
- `TELEGRAM_BOT_TOKEN` is filled in.
- You are not only editing `config.example.txt`.

### Telegram chat not found

If Telegram says `chat not found`, open your bot in Telegram and send:

```text
/start
test123
```

Then run the program again.

### Browser does not open immediately

The first run can take 30 seconds to 1 minute before Edge appears. Wait patiently.

If it still does not open, close the program, close all Microsoft Edge and `msedgedriver.exe` processes in Task Manager, then run the program again.

### Multiple windows were opened

Do not double-click the program repeatedly. Keep only one instance running.

---

## Limitations

This program only performs low-frequency page checking and Telegram notification.

It does not:

- automatically reserve a room;
- bypass login;
- bypass captcha;
- bypass access control;
- bypass any security mechanism;
- guarantee room availability.

Use it responsibly with your own CESAL resident account.

---

# 中文说明

[English](#cesal-room-monitor) | 中文说明

CESAL Room Monitor 是一个 Windows 绿色版 CESAL 房源监控工具。它会打开 Microsoft Edge，在需要时让用户手动登录 CESAL，然后低频检测 residence 是否有房，并在有房或检测结果变化时通过 Telegram 通知用户。

> 本项目仅用于个人低频监控自己的 CESAL resident account。它不会绕过登录、验证码、访问控制或任何安全机制。它不会自动预订房间。

---

## 这个项目能做什么

- 使用 Microsoft Edge 打开 CESAL resident 页面。
- 当 CESAL 要求登录时，让用户手动登录。
- 监控期间复用同一个浏览器会话。
- 打开 CESAL reservation 页面。
- 自动选择页面上显示的最新 arrival date。
- 自动填写配置中的租期结束日期。
- 点击 `Valider`。
- 读取各个 residence 的可用房间结果。
- 当有房或结果发生变化时，通过 Telegram 发送通知。
- 使用可配置的随机检测间隔，例如 6 到 12 分钟。
- 在本地写入运行日志和通知状态。

---

## 推荐使用方式：Windows 绿色版 Release

普通用户推荐从 GitHub Releases 下载 Windows 绿色版。

绿色版不需要安装 Python、Anaconda、pip，也不需要手动安装依赖。

你只需要：

- Windows
- Microsoft Edge
- Telegram
- 有效的 CESAL resident account

### 下载方式

进入：

```text
Releases -> latest version -> Assets
```

下载：

```text
CESALRoomMonitor_Windows_NoPython.zip
```

解压到本地文件夹。

解压后应该能看到类似这些文件：

```text
CESALRoomMonitor.exe
config.example.txt
README_FIRST_USE.txt
logs/
state/
```

---

## 第一次配置

### 第一步：创建 `config.txt`

复制：

```text
config.example.txt
```

把复制后的文件改名为：

```text
config.txt
```

不要直接修改 `config.example.txt`。你的私人配置应该写在 `config.txt` 里。

### 第二步：修改必须配置项

用记事本或其他文本编辑器打开 `config.txt`。

通常只需要修改：

```text
CESAL_END_DATE=19/06/2027
TELEGRAM_BOT_TOKEN=PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE
```

如果默认租期结束日期已经正确，那么只需要填写 `TELEGRAM_BOT_TOKEN`。

### 第三步：修改检测间隔

默认检测间隔是：

```text
CHECK_INTERVAL_MINUTES_MIN=6
CHECK_INTERVAL_MINUTES_MAX=12
```

意思是每次检测结束后，程序会随机等待 6 到 12 分钟再进行下一次检测。

你可以改成：

```text
CHECK_INTERVAL_MINUTES_MIN=10
CHECK_INTERVAL_MINUTES_MAX=20
```

不建议设置得太频繁，不建议低于 5 分钟。

---

## 如何获取 Telegram bot token

1. 打开 Telegram。
2. 搜索 `@BotFather`。
3. 打开和 BotFather 的聊天窗口。
4. 发送：

```text
/newbot
```

5. 按提示操作。
6. BotFather 会要求你设置机器人的显示名称和 username。
7. 机器人的 username 必须以 `bot` 结尾，例如：

```text
cesal_room_alert_abc_bot
```

8. 创建成功后，BotFather 会给你一串 token，格式类似：

```text
123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

9. 把这串 token 复制到 `config.txt`：

```text
TELEGRAM_BOT_TOKEN=123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

重要：Telegram bot token 是私人信息。不要把 `config.txt` 上传到 GitHub，也不要分享你的真实 token。

---

## 唤醒 Telegram 机器人

运行程序前，打开你的 Telegram 机器人聊天窗口，发送：

```text
/start
```

然后发送：

```text
test123
```

这是必须的，因为 Telegram 机器人不能主动给从未和它对话过的用户发送消息。

建议每天重新运行监控程序前，再发送一次 `test123`。这样程序更容易自动发现你的最新 Telegram chat ID。

---

## 运行程序

双击：

```text
CESALRoomMonitor.exe
```

首先会打开一个黑色命令行窗口。程序初始化完成后，Microsoft Edge 会自动打开。

### 第一次运行可能比较慢

第一次运行可能需要等待大约 30 秒到 1 分钟，Edge 浏览器才会弹出。请耐心等待，不要连续重复双击程序。

如果不小心打开了多个程序窗口，请关闭多余窗口，只保留一个程序运行。

### 手动登录 CESAL

如果 CESAL 要求登录：

1. 切换到自动打开的 Microsoft Edge 浏览器。
2. 手动登录你的 CESAL resident account。
3. 如果 Edge 询问是否保存密码，在你自己的可信电脑上可以选择保存或记住密码。
4. 等到 CESAL resident homepage 或 resident area 完全显示出来。
5. 回到黑色命令行窗口。
6. 按 `Enter` 继续。

### 程序怎么知道你已经登录成功

程序不会读取你的密码，也不会自动提交账号密码。

当程序检测到 CESAL 登录页面时，它会暂停并等待你手动登录。你在浏览器里登录成功后，需要回到黑色命令行窗口按 `Enter`，等于告诉程序“我已经登录完成”。然后程序会重新打开 reservation 页面。

如果此时仍然停留在登录页面，程序会再次提示你手动登录。

### 输入账号密码有时间限制吗

程序本身在等待登录时没有很短的倒计时。正常情况下，你可以花几分钟输入账号、密码，以及完成 CESAL 网站要求的验证。

但是 CESAL 网站自己可能有登录页面超时或 session 超时机制。如果网页超时了，就刷新或重新登录；等 resident 页面正常显示后，再回到命令行窗口按 `Enter`。

---

## 如何停止

在黑色命令行窗口中按：

```text
Ctrl + C
```

如果终端询问是否停止程序，确认即可。

---

## 仓库结构

```text
CESALRoomMonitor/
├── .github/workflows/              # GitHub Actions 自动打包 workflow
├── check_cesal_rooms.py            # 主监控脚本
├── config.example.txt              # 公开配置模板
├── README.md                       # 仓库首页说明
├── README_FIRST_USE.txt            # Release 用户第一次使用说明
├── requirements.txt                # 开发/打包依赖
├── environment.yml                 # 可选 Conda 环境文件
├── BUILD_EXE_ON_WINDOWS.bat        # 可选 Windows 本地打包脚本
├── LICENSE                         # 许可证文件
├── logs/                           # 本地运行日志
└── state/                          # 本地通知状态
```

---

## 使用 GitHub Actions 构建 Windows exe

本仓库已经包含 GitHub Actions workflow。

1. 把源码 push 到 GitHub。
2. 打开仓库页面。
3. 进入：

```text
Actions -> Build Windows EXE
```

4. 点击：

```text
Run workflow
```

5. 等待 workflow 成功。
6. 打开成功的 workflow run。
7. 下载 artifact：

```text
CESALRoomMonitor_Windows_NoPython
```

该 artifact 是包含 Windows 绿色版的 zip 文件。

---

## 发布 GitHub Release

从 GitHub Actions 下载 artifact 后，建议发布到 Release，这样普通用户更容易下载。

推荐流程：

1. 打开仓库页面。
2. 进入 `Releases`。
3. 点击 `Draft a new release`。
4. 设置 tag，例如：

```text
v1.0.0
```

5. 设置 release title，例如：

```text
CESAL Room Monitor v1.0.0
```

6. 上传 artifact zip 作为 release asset。
7. 点击 `Publish release`。

普通用户应该从下面位置下载软件：

```text
Releases -> latest version -> Assets
```

不需要下载源码。

---

## 本地开发

如果开发者想直接运行源码：

```bash
conda env create -f environment.yml
conda activate cesal_bot
python check_cesal_rooms.py
```

或者使用 pip：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python check_cesal_rooms.py
```

在 Windows 本地打包：

```text
BUILD_EXE_ON_WINDOWS.bat
```

普通用户不需要本地开发，直接使用 Release 版本即可。

---

## 隐私与安全

不要上传这些文件：

```text
config.txt
.env
logs/*
state/*
```

`config.example.txt` 可以分享，因为里面只有占位符。

`config.txt` 是私人文件，因为里面有你的真实 Telegram bot token。

如果 Telegram token 被意外上传或分享，请立即在 `@BotFather` 中 revoke，然后生成新的 token。

---

## 常见问题

### Telegram token 没有配置

如果程序提示 Telegram token 没有配置，请检查：

- `config.txt` 是否和 `CESALRoomMonitor.exe` 在同一个文件夹；
- `TELEGRAM_BOT_TOKEN` 是否已经填写；
- 你是不是只修改了 `config.example.txt`。

### Telegram chat not found

如果 Telegram 提示 `chat not found`，打开你的机器人聊天窗口并发送：

```text
/start
test123
```

然后重新运行程序。

### 浏览器没有立刻打开

第一次运行可能需要 30 秒到 1 分钟 Edge 才会弹出，请耐心等待。

如果一直没有打开，关闭程序，在任务管理器里关闭所有 Microsoft Edge 和 `msedgedriver.exe` 进程，然后重新运行程序。

### 打开了多个窗口

不要连续重复双击程序。只保留一个程序运行。

---

## 限制说明

本程序只做低频页面检测和 Telegram 通知。

它不会：

- 自动预订房间；
- 绕过登录；
- 绕过验证码；
- 绕过访问控制；
- 绕过任何安全机制；
- 保证一定有房。

请只用于你自己的 CESAL resident account，并合理低频使用。
