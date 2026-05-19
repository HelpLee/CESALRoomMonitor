CESAL Room Monitor - 最简单使用说明
===================================

目标：最终用户本地不需要安装 Python，只需要运行 exe。

一、普通用户怎么用 exe
---------------------

1. 下载 Windows_NoPython 版本压缩包并解压。

2. 找到 config.example.txt，复制一份并改名为：

   config.txt

3. 打开 config.txt，只改这两项：

   CESAL_END_DATE=19/06/2027
   TELEGRAM_BOT_TOKEN=你的Telegram机器人token

   检测间隔默认是：

   CHECK_INTERVAL_MINUTES_MIN=6
   CHECK_INTERVAL_MINUTES_MAX=12

   意思是每次检查结束后，随机等待 6 到 12 分钟再检查一次。

4. 创建 Telegram 机器人：

   - 打开 Telegram
   - 搜索 @BotFather
   - 发送 /newbot
   - 按提示设置名字
   - BotFather 会返回一串 token，例如：

     123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx

   - 把这串 token 填到 config.txt 里的 TELEGRAM_BOT_TOKEN 后面。

5. 唤醒机器人：

   打开你创建的机器人聊天窗口，发送：

   /start

   然后再发送：

   test123

   建议每天重新运行前，也发一次 test123。

6. 双击运行：

   CESALRoomMonitor.exe

7. 如果打开 Edge 后要求登录 CESAL，请在 Edge 里手动登录。
   登录完成后，回到黑色命令行窗口，按 Enter 继续。

8. 程序会自动循环检测，有房或状态变化时通过 Telegram 通知你。


二、怎么停止
------------

在黑色命令行窗口按：

Ctrl + C


三、重要说明
------------

- 不要把 config.txt 上传到 GitHub，因为里面有你的 Telegram token。
- 可以上传 config.example.txt，因为它只有占位符。
- 程序不会自动抢房，也不会绕过登录，只是帮你低频检测页面并通知。
- 电脑仍然需要安装 Microsoft Edge。Python 不需要用户安装。
