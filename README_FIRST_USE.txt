CESAL Room Monitor - First Use Guide / 绿色版第一次使用说明
===============================================================

English | 中文说明

This file is for users who have already downloaded the Windows portable package:

    CESALRoomMonitor_v1.0.0.zip

If you only want to use the program, follow this file.
You do not need to install Python, Anaconda, pip, or any Python package.

本文件适用于已经下载 Windows 绿色版压缩包的用户：

    CESALRoomMonitor_v1.0.0.zip

如果你只是想直接使用软件，按照本文件操作即可。
你不需要安装 Python、Anaconda、pip 或任何 Python 依赖。


1. What you need / 使用前需要准备什么
-------------------------------------

English:
Before using this program, make sure you have:

1. Windows computer
2. Microsoft Edge installed
3. Telegram account
4. A valid CESAL resident account
5. The extracted folder:

       CESALRoomMonitor_v1.0.0

The program needs Microsoft Edge because it opens the CESAL website in Edge and lets you log in manually.

中文：
使用前请确认你已经有：

1. Windows 电脑
2. 已安装 Microsoft Edge
3. Telegram 账号
4. 有效的 CESAL resident account
5. 已解压后的文件夹：

       CESALRoomMonitor_v1.0.0

程序需要 Microsoft Edge，因为它会用 Edge 打开 CESAL 网站，并让你手动登录。


2. Extract the package / 解压压缩包
------------------------------------

English:
Download and extract:

    CESALRoomMonitor_v1.0.0.zip

After extraction, you should get a folder named:

    CESALRoomMonitor_v1.0.0

Inside the folder, you should see files similar to:

    CESALRoomMonitor.exe
    config.example.txt
    README_FIRST_USE.txt
    logs/
    state/

Do not run the exe directly before creating config.txt.

中文：
下载并解压：

    CESALRoomMonitor_v1.0.0.zip

解压后，你应该得到一个文件夹：

    CESALRoomMonitor_v1.0.0

文件夹里应该能看到类似这些文件：

    CESALRoomMonitor.exe
    config.example.txt
    README_FIRST_USE.txt
    logs/
    state/

在创建 config.txt 之前，不要直接运行 exe。


3. Create config.txt / 创建 config.txt
---------------------------------------

English:
Inside the folder:

    CESALRoomMonitor_v1.0.0

Find:

    config.example.txt

Copy this file and rename the copied file to:

    config.txt

Important:
Do not rename config.example.txt directly.
Keep config.example.txt as a template.
Use config.txt for your own private settings.

中文：
在文件夹：

    CESALRoomMonitor_v1.0.0

里面找到：

    config.example.txt

复制这个文件，并把复制出来的文件改名为：

    config.txt

重要：
不要直接把 config.example.txt 改名。
请保留 config.example.txt 作为模板。
你的私人配置写在 config.txt 里。


4. Edit config.txt / 修改 config.txt
-------------------------------------

English:
Open config.txt with Notepad.

Usually, you only need to edit this line:

    TELEGRAM_BOT_TOKEN=PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE

Replace the placeholder with your real Telegram bot token.

You may also confirm this line:

    CESAL_END_DATE=19/06/2027

If 19/06/2027 is the lease end date you want to search for, you do not need to change it.
The date format must be:

    DD/MM/YYYY

Example:

    CESAL_END_DATE=19/06/2027

中文：
用记事本打开 config.txt。

通常你只需要修改这一行：

    TELEGRAM_BOT_TOKEN=PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE

把占位内容替换成你的真实 Telegram bot token。

你也可以顺便确认这一行：

    CESAL_END_DATE=19/06/2027

如果 19/06/2027 就是你希望查询的租期结束日期，那么不需要修改。
日期格式必须是：

    日/月/年

例如：

    CESAL_END_DATE=19/06/2027


5. Check interval / 检测间隔
----------------------------

English:
The default check interval is:

    CHECK_INTERVAL_MINUTES_MIN=6
    CHECK_INTERVAL_MINUTES_MAX=12

This means:
After each check, the program randomly waits 6 to 12 minutes before checking again.

You can change it, for example:

    CHECK_INTERVAL_MINUTES_MIN=10
    CHECK_INTERVAL_MINUTES_MAX=20

This means the program checks every 10 to 20 minutes.

Recommendation:
Do not set the interval lower than 5 minutes.
This tool is designed for low-frequency personal monitoring.

中文：
默认检测间隔是：

    CHECK_INTERVAL_MINUTES_MIN=6
    CHECK_INTERVAL_MINUTES_MAX=12

意思是：
每次检测结束后，程序会随机等待 6 到 12 分钟，再进行下一次检测。

你可以改成：

    CHECK_INTERVAL_MINUTES_MIN=10
    CHECK_INTERVAL_MINUTES_MAX=20

这表示程序每 10 到 20 分钟检测一次。

建议：
不要设置低于 5 分钟。
这个工具是为个人低频监控设计的。


6. How to get the Telegram bot token / 如何获取 Telegram bot token
-------------------------------------------------------------------

English:
1. Open Telegram.
2. Search for:

       @BotFather

3. Open the chat with BotFather.
4. Send:

       /newbot

5. Follow the instructions.
6. BotFather will ask you to set:
   - a display name for your bot;
   - a username for your bot.

7. The bot username must end with:

       bot

   Example:

       cesal_room_alert_abc_bot

8. After the bot is created, BotFather will send you a token similar to:

       123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx

9. Copy that token into config.txt:

       TELEGRAM_BOT_TOKEN=123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Important:
The Telegram bot token is private.
Do not share it.
Do not upload config.txt to GitHub or send it to other people.

中文：
1. 打开 Telegram。
2. 搜索：

       @BotFather

3. 打开和 BotFather 的聊天窗口。
4. 发送：

       /newbot

5. 按提示操作。
6. BotFather 会要求你设置：
   - 机器人的显示名称；
   - 机器人的 username。

7. 机器人的 username 必须以：

       bot

   结尾。

   例如：

       cesal_room_alert_abc_bot

8. 创建成功后，BotFather 会发给你一串 token，格式类似：

       123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx

9. 把这串 token 填入 config.txt：

       TELEGRAM_BOT_TOKEN=123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx

重要：
Telegram bot token 是私人信息。
不要分享它。
不要把 config.txt 上传到 GitHub，也不要发给别人。


7. Wake up your Telegram bot / 唤醒 Telegram 机器人
---------------------------------------------------

English:
Before running CESALRoomMonitor.exe, open your own Telegram bot chat and send:

    /start

Then send:

    test123

This step is required.
A Telegram bot cannot send messages to you until you start a chat with it.

Recommended:
Before running the monitor each day, send:

    test123

again to your bot.
This helps the program discover your latest Telegram chat ID automatically.

中文：
运行 CESALRoomMonitor.exe 之前，打开你自己的 Telegram 机器人聊天窗口，发送：

    /start

然后发送：

    test123

这一步是必须的。
Telegram 机器人不能主动给从未和它对话过的用户发送消息。

建议：
每天重新运行监控程序前，再给机器人发送一次：

    test123

这样程序更容易自动发现你的最新 Telegram chat ID。


8. Run the program / 运行程序
-----------------------------

English:
Inside the folder:

    CESALRoomMonitor_v1.0.0

Double-click:

    CESALRoomMonitor.exe

A black command window will open first.
Microsoft Edge will open automatically after initialization.

Important:
The first run may be slow.
It may take about 30 seconds to 1 minute before the Edge browser appears.
Please wait patiently.
Do not double-click the program repeatedly.

If you accidentally open several program windows, close the extra windows and keep only one instance running.

中文：
在文件夹：

    CESALRoomMonitor_v1.0.0

里面双击：

    CESALRoomMonitor.exe

首先会打开一个黑色命令行窗口。
程序初始化完成后，Microsoft Edge 会自动打开。

重要：
第一次运行可能比较慢。
Edge 浏览器可能需要等待大约 30 秒到 1 分钟才会弹出。
请耐心等待。
不要连续重复双击程序。

如果不小心打开了多个程序窗口，请关闭多余窗口，只保留一个程序运行。


9. Manual CESAL login / 手动登录 CESAL
--------------------------------------

English:
If CESAL asks you to log in:

1. Go to the opened Microsoft Edge browser.
2. Log in to your CESAL resident account manually.
3. If Edge asks whether to save the password, you may choose to save or remember the password on your own trusted computer.
4. Wait until the CESAL resident homepage or resident area is fully visible.
5. Return to the black command window.
6. Press Enter to continue.

中文：
如果 CESAL 要求登录：

1. 切换到自动打开的 Microsoft Edge 浏览器。
2. 手动登录你的 CESAL resident account。
3. 如果 Edge 询问是否保存密码，在你自己的可信电脑上可以选择保存或记住密码。
4. 等到 CESAL resident homepage 或 resident area 完全显示出来。
5. 回到黑色命令行窗口。
6. 按 Enter 继续。


10. How does the program know login is complete? / 程序怎么知道你登录成功？
--------------------------------------------------------------------------

English:
The program does not read your password.
It does not automatically submit login credentials.

When the program detects the CESAL login page, it pauses and waits.
After you manually log in, you must return to the black command window and press Enter.
Pressing Enter tells the program that you have finished logging in.

Then the program opens the reservation page again.
If it is still on the login page, the program will ask you to log in again.

中文：
程序不会读取你的密码。
程序也不会自动提交账号密码。

当程序检测到 CESAL 登录页面时，它会暂停等待。
你在浏览器里手动登录成功后，需要回到黑色命令行窗口并按 Enter。
按 Enter 等于告诉程序你已经完成登录。

然后程序会重新打开 reservation 页面。
如果此时仍然停留在登录页面，程序会再次提示你手动登录。


11. Is there a time limit for entering the password? / 输入账号密码有时间限制吗？
--------------------------------------------------------------------------------

English:
The program itself does not set a short countdown while waiting for login.
Normally, you can take several minutes to enter your username, password, and any verification required by CESAL.

However, the CESAL website may have its own login page timeout or session timeout.
If the webpage expires, refresh it or log in again.
After the resident page is visible, return to the command window and press Enter.

中文：
程序本身在等待登录时没有很短的倒计时。
正常情况下，你可以花几分钟输入账号、密码，以及完成 CESAL 网站要求的验证。

但是 CESAL 网站自己可能有登录页面超时或 session 超时机制。
如果网页超时了，就刷新或重新登录。
等 resident 页面正常显示后，再回到命令行窗口按 Enter。


12. What happens after login / 登录之后程序会做什么
---------------------------------------------------

English:
After login, the program will automatically:

1. Open the CESAL reservation page.
2. Select the latest available arrival date shown by the page.
3. Fill in your configured lease end date.
4. Click Valider.
5. Read the availability result for each residence.
6. Send a Telegram notification when availability is found or when the result changes.
7. Wait for the configured random interval.
8. Repeat the check.

中文：
登录完成后，程序会自动：

1. 打开 CESAL reservation 页面。
2. 选择页面上显示的最新 arrival date。
3. 填写你配置的租期结束日期。
4. 点击 Valider。
5. 读取各个 residence 的可用房间结果。
6. 如果发现有房或结果发生变化，就通过 Telegram 通知你。
7. 随机等待你设置的检测间隔。
8. 重复检测。


13. How to stop / 如何停止
--------------------------

English:
In the black command window, press:

    Ctrl + C

If Windows asks whether to terminate the program, confirm it.

中文：
在黑色命令行窗口中按：

    Ctrl + C

如果 Windows 询问是否终止程序，确认即可。


14. Privacy and safety / 隐私与安全
-----------------------------------

English:
config.example.txt is safe to share because it only contains placeholders.

config.txt is private because it contains your real Telegram bot token.
Do not upload config.txt to GitHub.
Do not send config.txt to other people.

logs/ contains runtime logs.
state/ contains notification state.

If your Telegram token is accidentally shared, open @BotFather, revoke the token, and generate a new one.

中文：
config.example.txt 可以分享，因为里面只有占位符。

config.txt 是私人文件，因为里面有你的真实 Telegram bot token。
不要把 config.txt 上传到 GitHub。
不要把 config.txt 发给别人。

logs/ 里面是运行日志。
state/ 里面是通知状态。

如果你的 Telegram token 被意外分享，请打开 @BotFather，撤销旧 token，并生成新的 token。


15. Troubleshooting / 常见问题
------------------------------

English:

Problem: Telegram token is not configured.
Check:
- config.txt exists in the same folder as CESALRoomMonitor.exe.
- TELEGRAM_BOT_TOKEN has been filled in.
- You are not only editing config.example.txt.

Problem: Telegram says chat not found.
Solution:
Open your Telegram bot chat and send:

    /start
    test123

Then run the program again.

Problem: Edge does not open immediately.
Solution:
Wait 30 seconds to 1 minute on the first run.
If it still does not open, close the program, close all Microsoft Edge and msedgedriver.exe processes in Task Manager, then run it again.

Problem: Several black windows were opened.
Solution:
Close the extra windows and keep only one CESALRoomMonitor.exe running.

中文：

问题：程序提示 Telegram token 没有配置。
检查：
- config.txt 是否和 CESALRoomMonitor.exe 在同一个文件夹。
- TELEGRAM_BOT_TOKEN 是否已经填写。
- 你是不是只修改了 config.example.txt。

问题：Telegram 提示 chat not found。
解决：
打开你的 Telegram 机器人聊天窗口，发送：

    /start
    test123

然后重新运行程序。

问题：Edge 没有立刻打开。
解决：
第一次运行请等待 30 秒到 1 分钟。
如果仍然没有打开，关闭程序，在任务管理器里关闭所有 Microsoft Edge 和 msedgedriver.exe 进程，然后重新运行。

问题：打开了多个黑色窗口。
解决：
关闭多余窗口，只保留一个 CESALRoomMonitor.exe 运行。


16. Important limitations / 重要限制
------------------------------------

English:
This program only performs low-frequency page checking and Telegram notification.

It does not:
- automatically reserve a room;
- bypass login;
- bypass captcha;
- bypass access control;
- bypass any security mechanism;
- guarantee room availability.

Use it responsibly with your own CESAL resident account.

中文：
本程序只做低频页面检测和 Telegram 通知。

它不会：
- 自动预订房间；
- 绕过登录；
- 绕过验证码；
- 绕过访问控制；
- 绕过任何安全机制；
- 保证一定有房。

请只用于你自己的 CESAL resident account，并合理低频使用。
