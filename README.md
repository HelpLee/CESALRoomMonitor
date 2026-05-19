# CESAL Room Monitor - Simple Windows No-Python Version

这是一个最小配置版本。目标是：**最终用户本地不需要安装 Python**，只运行 `CESALRoomMonitor.exe`。

> 注意：本仓库源码仍然是 Python。要得到 exe，有两种方式：
>
> 1. 推荐：上传到 GitHub 后，由 GitHub Actions 自动构建 Windows exe。本地不需要 Python。
> 2. 开发者方式：在 Windows 本地用 Python + PyInstaller 打包。

## 最简单配置

最终发布包里只需要这些文件：

```text
CESALRoomMonitor.exe
config.example.txt
README_FIRST_USE.txt
logs/
state/
```

用户只需要：

1. 复制 `config.example.txt`，改名为 `config.txt`。
2. 打开 `config.txt`，只改：

```text
CESAL_END_DATE=19/06/2027
TELEGRAM_BOT_TOKEN=你的BotFather token
```

默认每 6 到 12 分钟随机检测一次：

```text
CHECK_INTERVAL_MINUTES_MIN=6
CHECK_INTERVAL_MINUTES_MAX=12
```

一般不需要改其他参数。

## Telegram token 怎么获取

1. 打开 Telegram。
2. 搜索 `@BotFather`。
3. 发送 `/newbot`。
4. 按提示设置 bot 名字和 username。
5. BotFather 会返回一串 token，例如：

```text
123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

把它填到 `config.txt`：

```text
TELEGRAM_BOT_TOKEN=123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Telegram chat_id 怎么处理

本版本默认自动发现 chat_id，不需要手填。

运行前请先给你的 bot 发送：

```text
/start
```

然后发送：

```text
test123
```

建议每天运行前也发一次 `test123`，这样 Telegram `getUpdates` 能拿到最新消息，程序能自动识别你的 chat_id。

## 修改检测间隔

打开 `config.txt`，改这一行：

```text
CHECK_INTERVAL_MINUTES_MIN=6
CHECK_INTERVAL_MINUTES_MAX=12
```

例如每 10 到 20 分钟随机检测一次：

```text
CHECK_INTERVAL_MINUTES_MIN=10
CHECK_INTERVAL_MINUTES_MAX=20
```

不建议低于 5 分钟。

## GitHub Actions 自动生成 exe

本仓库已经包含：

```text
.github/workflows/build-windows-exe.yml
```

使用方式：

1. 新建 GitHub 仓库。
2. 上传本仓库所有文件。
3. 进入 GitHub 页面：`Actions`。
4. 选择 `Build Windows EXE`。
5. 点击 `Run workflow`。
6. 等待完成后，在 workflow 结果页面下载 artifact：

```text
CESALRoomMonitor_Windows_NoPython
```

下载并解压后，里面就是无需安装 Python 的 Windows 绿色版。

## 本地开发者打包方式

如果你愿意在 Windows 本地安装 Python，可以运行：

```bat
BUILD_EXE_ON_WINDOWS.bat
```

它会生成：

```text
release\CESALRoomMonitor_Windows_NoPython.zip
```

普通用户不需要这一步。

## 安全说明

不要提交这些文件：

```text
config.txt
.env
logs/
state/
```

`config.txt` 里有你的 Telegram token，不能上传公开仓库。
