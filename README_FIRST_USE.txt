CESAL Room Monitor - First Use Guide / 最简单使用说明
=====================================================

Purpose / 目标
--------------

English:
This is the Windows portable version of CESAL Room Monitor.
The final user does not need to install Python, Anaconda, pip, or any Python package.
You only need Microsoft Edge, Telegram, and the executable file.

中文：
这是 CESAL Room Monitor 的 Windows 绿色版。
最终用户本地不需要安装 Python、Anaconda、pip 或任何 Python 依赖。
只需要电脑上有 Microsoft Edge、Telegram，以及本软件的 exe 文件。


1. Download and extract / 下载并解压
------------------------------------

English:
Download the Windows portable zip file:

    CESALRoomMonitor_Windows_NoPython.zip

Then extract it to any local folder, for example:

    C:\Users\YourName\Desktop\CESALRoomMonitor

After extraction, you should see files similar to:

    CESALRoomMonitor.exe
    config.example.txt
    README_FIRST_USE.txt
    logs/
    state/

中文：
下载 Windows 绿色版压缩包：

    CESALRoomMonitor_Windows_NoPython.zip

然后解压到任意本地文件夹，例如：

    C:\Users\YourName\Desktop\CESALRoomMonitor

解压后，你应该能看到类似这些文件：

    CESALRoomMonitor.exe
    config.example.txt
    README_FIRST_USE.txt
    logs/
    state/


2. Create your local config file / 创建本地配置文件
--------------------------------------------------

English:
Find this file:

    config.example.txt

Copy it, and rename the copied file to:

    config.txt

Important:
Do not edit config.example.txt directly.
Use config.txt for your own private settings.

中文：
找到这个文件：

    config.example.txt

复制一份，并把复制后的文件改名为：

    config.txt

重要：
不要直接修改 config.example.txt。
你的私人配置应该写在 config.txt 里。


3. Edit the required settings / 修改必须配置项
----------------------------------------------

English:
Open config.txt with Notepad or any text editor.
Normally, you only need to edit these two lines:

    CESAL_END_DATE=19/06/2027
    TELEGRAM_BOT_TOKEN=PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE

Explanation:

    CESAL_END_DATE

This is the lease end date you want to search for.
The format must be day/month/year:

    DD/MM/YYYY

Example:

    19/06/2027

    TELEGRAM_BOT_TOKEN

This is the token of your Telegram bot.
You will get it from Telegram's @BotFather.

中文：
用记事本或其他文本编辑器打开 config.txt。
通常只需要修改下面两行：

    CESAL_END_DATE=19/06/2027
    TELEGRAM_BOT_TOKEN=PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE

解释：

    CESAL_END_DATE

这是你希望查询的租期结束日期。
格式必须是 日/月/年：

    日/月/年

例如：

    19/06/2027

    TELEGRAM_BOT_TOKEN

这是你的 Telegram 机器人 token。
它需要从 Telegram 的 @BotFather 获取。


4. How to get the Telegram bot token / 如何获取 Telegram bot token
-------------------------------------------------------------------

English:
1. Open Telegram.
2. Search for:

       @BotFather

3. Open the chat with BotFather.
4. Send:

       /newbot

5. Follow the instructions.
   BotFather will ask you to set:
   - a display name for your bot;
   - a username for your bot.

6. The bot username must end with:

       bot

   Example:

       cesal_room_alert_abc_bot

7. After the bot is created, BotFather will send you a token similar to:

       123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx

8. Copy that token and paste it into config.txt:

       TELEGRAM_BOT_TOKEN=123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Important:
The Telegram bot token is a private password.
Do not upload config.txt to GitHub.
Do not share your real token with other people.

中文：
1. 打开 Telegram。
2. 搜索：

       @BotFather

3. 打开和 BotFather 的聊天窗口。
4. 发送：

       /newbot

5. 按提示操作。
   BotFather 会要求你设置：
   - 机器人的显示名称；
   - 机器人的 username。

6. 机器人的 username 必须以：

       bot

   结尾。

   例如：

       cesal_room_alert_abc_bot

7. 创建成功后，BotFather 会发给你一串 token，格式类似：

       123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx

8. 复制这串 token，填入 config.txt：

       TELEGRAM_BOT_TOKEN=123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx

重要：
Telegram bot token 相当于密码。
不要把 config.txt 上传到 GitHub。
不要把你的真实 token 分享给别人。


5. Wake up the Telegram bot / 唤醒 Telegram 机器人
--------------------------------------------------

English:
Before running the program, open your own Telegram bot chat and send:

    /start

Then send:

    test123

This step is necessary because a Telegram bot cannot send messages to you until you have started a chat with it.

Recommended:
Before you run the monitor each day, send the bot one message again:

    test123

This helps the program discover your latest Telegram chat id automatically.

中文：
运行程序之前，打开你自己的 Telegram 机器人聊天窗口，发送：

    /start

然后再发送：

    test123

这一步是必须的，因为 Telegram 机器人不能主动给从未和它对话过的用户发送消息。

建议：
每天重新运行监控程序之前，再给机器人发送一次：

    test123

这样程序更容易自动发现你的最新 Telegram chat id。


6. Check interval settings / 检测间隔设置
-----------------------------------------

English:
The default check interval is a random value between 6 and 12 minutes:

    CHECK_INTERVAL_MINUTES_MIN=6
    CHECK_INTERVAL_MINUTES_MAX=12

This means:
After each check, the program randomly waits 6 to 12 minutes before the next check.

You can change it, for example:

    CHECK_INTERVAL_MINUTES_MIN=10
    CHECK_INTERVAL_MINUTES_MAX=20

This means the program checks every 10 to 20 minutes.

Recommendation:
Do not set the interval too short.
A value lower than 5 minutes is not recommended.

中文：
默认检测间隔是在 6 到 12 分钟之间随机选择：

    CHECK_INTERVAL_MINUTES_MIN=6
    CHECK_INTERVAL_MINUTES_MAX=12

意思是：
每次检测结束后，程序会随机等待 6 到 12 分钟，再进行下一次检测。

你可以修改，例如：

    CHECK_INTERVAL_MINUTES_MIN=10
    CHECK_INTERVAL_MINUTES_MAX=20

这表示程序每 10 到 20 分钟检测一次。

建议：
不要设置得太频繁。
不建议低于 5 分钟。


7. Run the program / 运行程序
-----------------------------

English:
Double-click:

    CESALRoomMonitor.exe

A black command window will open first.
Microsoft Edge will open automatically after the program finishes initialization.

Important for the first run:
The first run can be slow. It may take about 30 seconds to 1 minute before the Edge browser appears.
Please wait patiently and do not double-click the program repeatedly.
If several program windows are opened at the same time, close the extra windows and keep only one instance running.

If CESAL asks you to log in:
1. Go to the opened Microsoft Edge browser.
2. Log in to your CESAL resident account manually.
3. If Edge asks whether to save the password, it is recommended to choose save or remember password on your own trusted computer.
   This can make future manual login easier.
4. Wait until the CESAL resident homepage or resident area is fully visible.
5. Return to the black command window.
6. Press Enter to continue.

How the program knows that login is complete:
The program cannot read your password and does not automatically submit login credentials.
When it detects the CESAL login page, it pauses and waits for you.
After you manually log in, you confirm completion by pressing Enter in the black command window.
Then the program opens the reservation page again.
If it is still on the login page, the program will ask you to log in again.

How long do you have to enter the password:
There is no short program-side countdown while the program is waiting at the login prompt.
In normal use, you can take several minutes to enter the username, password, and any verification required by CESAL.
However, the CESAL website itself may have its own session timeout or login timeout.
If the website expires the login page, refresh or log in again, then return to the command window and press Enter after the resident page is visible.

After login, the program will:
1. open the CESAL reservation page;
2. select the latest available arrival date shown by the page;
3. fill in your configured lease end date;
4. click Valider;
5. read the residence availability result;
6. send a Telegram notification when availability is found or when the result changes;
7. wait for the configured random interval;
8. repeat the check.

中文：
双击运行：

    CESALRoomMonitor.exe

首先会打开一个黑色命令行窗口。
程序初始化完成后，Microsoft Edge 会自动打开。

第一次运行的重要说明：
第一次运行可能比较慢，Edge 浏览器可能需要等待大约 30 秒到 1 分钟才会弹出。
请耐心等待，不要连续重复双击程序。
如果不小心打开了多个程序窗口，请关闭多余窗口，只保留一个程序运行。

如果 CESAL 要求登录：
1. 切换到自动打开的 Microsoft Edge 浏览器。
2. 手动登录你的 CESAL resident account。
3. 如果 Edge 询问是否保存密码，建议在你自己的可信电脑上选择保存或记住密码。
   这样以后手动登录会更方便。
4. 等到 CESAL resident homepage 或 resident area 完全显示出来。
5. 回到黑色命令行窗口。
6. 按 Enter 继续。

程序怎么知道你已经登录成功：
程序不会读取你的密码，也不会自动提交账号密码。
当程序检测到 CESAL 登录页面时，它会暂停并等待你手动登录。
你在浏览器里登录成功后，需要回到黑色命令行窗口按 Enter，等于告诉程序“我已经登录完成”。
然后程序会重新打开 reservation 页面。
如果此时仍然停留在登录页面，程序会再次提示你手动登录。

输入账号密码有时间限制吗：
程序本身在等待登录时没有很短的倒计时。
正常情况下，你可以花几分钟输入账号、密码，以及完成 CESAL 网站要求的验证。
但是 CESAL 网站自己可能有登录页面超时或 session 超时机制。
如果网页超时了，就刷新或重新登录；等 resident 页面正常显示后，再回到命令行窗口按 Enter。

登录完成后，程序会自动：
1. 打开 CESAL reservation 页面；
2. 选择页面上显示的最新 arrival date；
3. 填写你配置的租期结束日期；
4. 点击 Valider；
5. 读取各个 residence 的可用房间结果；
6. 如果发现有房或结果发生变化，就通过 Telegram 通知你；
7. 随机等待你设置的检测间隔；
8. 重复检测。


8. How to stop / 如何停止
-------------------------

English:
In the black command window, press:

    Ctrl + C

Then confirm if the terminal asks you to stop the program.

中文：
在黑色命令行窗口中按：

    Ctrl + C

如果终端询问是否停止程序，确认即可。


9. Files and privacy / 文件和隐私说明
-------------------------------------

English:
config.example.txt is safe to share because it only contains placeholders.

config.txt is private because it contains your real Telegram bot token.
Do not upload config.txt to GitHub.
Do not send config.txt to other people.

logs/ contains runtime logs.
state/ contains notification state.
These files are local runtime files and are not required for sharing the software.

中文：
config.example.txt 可以分享，因为里面只有占位符。

config.txt 是私人文件，因为里面有你的真实 Telegram bot token。
不要把 config.txt 上传到 GitHub。
不要把 config.txt 发给别人。

logs/ 里面是运行日志。
state/ 里面是通知状态。
这些都是本地运行文件，不需要随软件一起公开分享。


10. Important limitations / 重要限制
------------------------------------

English:
This program only performs low-frequency page checking and sends notifications.
It does not automatically reserve a room.
It does not bypass login, captcha, access control, or any security mechanism.
You must use it responsibly with your own CESAL resident account.

The computer still needs Microsoft Edge installed.
The final user does not need to install Python.

中文：
这个程序只做低频页面检测和通知。
它不会自动预订房间。
它不会绕过登录、验证码、访问控制或任何安全机制。
请只用于你自己的 CESAL resident account，并合理低频使用。

电脑上仍然需要安装 Microsoft Edge。
最终用户不需要安装 Python。
