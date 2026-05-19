# CESAL Room Monitor

English | [中文说明](#中文说明)

A lightweight Windows portable tool for monitoring the CESAL resident housing reservation page. It opens Microsoft Edge, lets the user log in manually when required, checks residence availability at a low frequency, and sends Telegram notifications when rooms are available or when the availability result changes.

> This project is for personal, low-frequency monitoring of your own CESAL resident account. It does not bypass login, captcha, access control, or any security mechanism. It does not automatically reserve a room.

---

## Which option should you choose?

There are two different ways to use this project.

### Option A: I only want to use the program

Use the Windows portable release.

You do not need to install Python, Anaconda, pip, or any Python package.

Go to:

```text
Releases -> latest version -> Assets
```

Download:

```text
CESALRoomMonitor_v1.0.0.zip
```

Extract it, then read the file inside the zip:

```text
README_FIRST_USE.txt
```

That file explains how to configure `config.txt`, how to get a Telegram bot token, how to send `/start` and `test123`, and how to run `CESALRoomMonitor.exe`.

This is the recommended option for normal users.

### Option B: I want to build or modify the project myself

Use the source code in this repository.

This option is for developers or users who want to:

- modify the Python script;
- change the build workflow;
- build a new exe with GitHub Actions;
- publish a new GitHub Release;
- run the source code directly with Python.

For this option, read the later sections:

- Repository structure
- Build the Windows executable with GitHub Actions
- Publish a GitHub Release
- Local development

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

## Direct use: Windows portable release

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

Download the Windows portable zip file, for example:

```text
CESALRoomMonitor_v1.0.0.zip
```

Extract it to a local folder.

After extraction, the folder should be named:

```text
CESALRoomMonitor_v1.0.0
```

Inside this folder, you should see files similar to:

```text
CESALRoomMonitor_v1.0.0/
├── CESALRoomMonitor.exe
├── config.example.txt
├── README_FIRST_USE.txt
├── logs/
└── state/
```

### Read the package guide first

The release zip includes:

```text
README_FIRST_USE.txt
```

This is the user guide for the packaged executable. Read it before running the program.

In short:

1. Copy `config.example.txt`.
2. Rename the copy to `config.txt`.
3. Fill in `TELEGRAM_BOT_TOKEN`.
4. Confirm or edit `CESAL_END_DATE`.
5. Send `/start` and `test123` to your Telegram bot.
6. Double-click `CESALRoomMonitor.exe`.

---

## First-time configuration summary

The full first-use guide is in `README_FIRST_USE.txt` inside the release zip. The following is only a summary.

### Step 1: Create `config.txt`

Inside the `CESALRoomMonitor_v1.0.0` folder, copy:

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

## Telegram bot setup summary

The full Telegram setup guide is in `README_FIRST_USE.txt` inside the release zip.

1. Open Telegram.
2. Search for `@BotFather`.
3. Send:

```text
/newbot
```

4. Follow the instructions.
5. Copy the token returned by BotFather.
6. Paste it into `config.txt`:

```text
TELEGRAM_BOT_TOKEN=123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Before running the program, open your Telegram bot chat and send:

```text
/start
test123
```

It is recommended to send `test123` again before running the monitor each day.

Important: the Telegram bot token is private. Do not upload `config.txt` to GitHub and do not share your real token.

---

## Running summary

The full running guide is in `README_FIRST_USE.txt`.

Inside the `CESALRoomMonitor_v1.0.0` folder, double-click:

```text
CESALRoomMonitor.exe
```

The first run may take about 30 seconds to 1 minute before the Edge browser appears.

If CESAL asks you to log in, log in manually in the opened Microsoft Edge browser. After the CESAL resident page is visible, return to the black command window and press `Enter` to continue.

The program does not read your password and does not automatically submit login credentials. It waits for you to complete the login manually.

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

The packaged Windows release folder is:

```text
CESALRoomMonitor_v1.0.0/
├── CESALRoomMonitor.exe
├── config.example.txt
├── README_FIRST_USE.txt
├── logs/
└── state/
```

---

## Build the Windows executable with GitHub Actions

This section is only needed if you want to build the program yourself.

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
7. Download the artifact.

The artifact should be published or renamed as:

```text
CESALRoomMonitor_v1.0.0.zip
```

This zip file contains the Windows portable version.

---

## Publish a GitHub Release

This section is only needed if you want other users to download your built executable easily.

After downloading the artifact from GitHub Actions, publish it as a Release.

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

6. Upload the Windows portable zip as a release asset:

```text
CESALRoomMonitor_v1.0.0.zip
```

7. Click `Publish release`.

Normal users should download the program from:

```text
Releases -> latest version -> Assets -> CESALRoomMonitor_v1.0.0.zip
```

They do not need to download the source code.

---

## Local development

This section is only needed if you want to run or modify the source code directly.

With Conda:

```bash
conda env create -f environment.yml
conda activate cesal_bot
python check_cesal_rooms.py
```

With pip:

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

## 应该选择哪种使用方式？

这个项目有两种使用方式。

### 方式 A：我只是想直接使用软件

请使用 Windows 绿色版 Release。

你不需要安装 Python、Anaconda、pip，也不需要安装任何 Python 包。

进入：

```text
Releases -> latest version -> Assets
```

下载：

```text
CESALRoomMonitor_v1.0.0.zip
```

解压后，阅读压缩包里的：

```text
README_FIRST_USE.txt
```

这个文件会说明如何配置 `config.txt`、如何获取 Telegram bot token、如何发送 `/start` 和 `test123`，以及如何运行 `CESALRoomMonitor.exe`。

这是普通用户最推荐的方式。

### 方式 B：我想自己构建或修改项目

请使用本仓库里的源代码。

这种方式适合开发者，或者适合想要做下面事情的用户：

- 修改 Python 脚本；
- 修改打包 workflow；
- 用 GitHub Actions 构建新的 exe；
- 发布新的 GitHub Release；
- 直接用 Python 运行源码。

如果你选择这种方式，请阅读后面的章节：

- 仓库结构
- 使用 GitHub Actions 构建 Windows exe
- 发布 GitHub Release
- 本地开发

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

## 直接使用：Windows 绿色版 Release

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

下载 Windows 绿色版压缩包，例如：

```text
CESALRoomMonitor_v1.0.0.zip
```

解压到本地文件夹。

解压后的文件夹名称应为：

```text
CESALRoomMonitor_v1.0.0
```

文件夹内部应类似：

```text
CESALRoomMonitor_v1.0.0/
├── CESALRoomMonitor.exe
├── config.example.txt
├── README_FIRST_USE.txt
├── logs/
└── state/
```

### 先阅读压缩包说明

Release 压缩包里包含：

```text
README_FIRST_USE.txt
```

这是打包 exe 的用户说明。运行前建议先阅读。

简短流程是：

1. 复制 `config.example.txt`。
2. 把复制后的文件改名为 `config.txt`。
3. 填写 `TELEGRAM_BOT_TOKEN`。
4. 确认或修改 `CESAL_END_DATE`。
5. 给 Telegram bot 发送 `/start` 和 `test123`。
6. 双击 `CESALRoomMonitor.exe`。

---

## 第一次配置概要

完整第一次使用说明在 Release 压缩包里的 `README_FIRST_USE.txt`。下面只是概要。

### 第一步：创建 `config.txt`

在 `CESALRoomMonitor_v1.0.0` 文件夹中，复制：

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

## Telegram bot 设置概要

完整 Telegram 配置说明在 Release 压缩包里的 `README_FIRST_USE.txt`。

1. 打开 Telegram。
2. 搜索 `@BotFather`。
3. 发送：

```text
/newbot
```

4. 按提示操作。
5. 复制 BotFather 返回的 token。
6. 把 token 填入 `config.txt`：

```text
TELEGRAM_BOT_TOKEN=123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

运行程序前，打开你的 Telegram 机器人聊天窗口，发送：

```text
/start
test123
```

建议每天重新运行监控程序前，再发送一次 `test123`。

重要：Telegram bot token 是私人信息。不要把 `config.txt` 上传到 GitHub，也不要分享你的真实 token。

---

## 运行概要

完整运行说明在 `README_FIRST_USE.txt`。

在 `CESALRoomMonitor_v1.0.0` 文件夹中，双击：

```text
CESALRoomMonitor.exe
```

第一次运行可能需要等待大约 30 秒到 1 分钟，Edge 浏览器才会弹出。

如果 CESAL 要求登录，请在自动打开的 Microsoft Edge 浏览器里手动登录。等 CESAL resident 页面正常显示后，回到黑色命令行窗口按 `Enter` 继续。

程序不会读取你的密码，也不会自动提交账号密码。它只会等待你手动完成登录。

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

打包后的 Windows 绿色版文件夹是：

```text
CESALRoomMonitor_v1.0.0/
├── CESALRoomMonitor.exe
├── config.example.txt
├── README_FIRST_USE.txt
├── logs/
└── state/
```

---

## 使用 GitHub Actions 构建 Windows exe

这一节只在你想自己构建程序时需要阅读。

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
7. 下载 artifact。

该 artifact 建议发布或重命名为：

```text
CESALRoomMonitor_v1.0.0.zip
```

这个 zip 文件包含 Windows 绿色版。

---

## 发布 GitHub Release

这一节只在你想让其他用户方便下载你的 exe 时需要阅读。

从 GitHub Actions 下载 artifact 后，建议发布到 Release。

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

6. 上传 Windows 绿色版 zip 作为 release asset：

```text
CESALRoomMonitor_v1.0.0.zip
```

7. 点击 `Publish release`。

普通用户应该从下面位置下载软件：

```text
Releases -> latest version -> Assets -> CESALRoomMonitor_v1.0.0.zip
```

不需要下载源码。

---

## 本地开发

这一节只在你想直接运行或修改源码时需要阅读。

使用 Conda：

```bash
conda env create -f environment.yml
conda activate cesal_bot
python check_cesal_rooms.py
```

使用 pip：

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
