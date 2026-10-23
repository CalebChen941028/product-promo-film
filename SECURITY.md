# Security · 安全

English first, 中文在后。

## English
### Reporting a problem
Please report a vulnerability privately through this repository's **Security → Report a vulnerability** page on GitHub (if it is not shown, open an issue that says you have a security report, without the details, and a maintainer will arrange a private channel). Please do not publish exploit details before there is a fix.

### What to know before you run it
Reelwright runs on your machine, sends nothing anywhere, and has no telemetry. Some features run code or touch files on purpose:
- **`film.json` is trusted input.** `"scripts"` and `"css"` run in a local Chromium (started with `--allow-file-access-from-files` so the page can read its own media). Only render films you wrote or have read.
- **`record_ui.mjs` recipes are trusted input.** `serve.cmd` runs a shell command you wrote, in the folder you named. It limits the recorded browser to localhost by default, uses an empty profile, and stops only the server it started.
- **`capture_app.mjs` launches installed apps.** It copies the app's profile into a temporary folder (never writes to the original); `"profile_extra": ["secrets"]` also copies its encrypted key store there, only when you ask for it, and the copy is deleted after the run. It never types a key or a password.
- **The download steps are explicit.** Models and voices are fetched only after you agree; installers copy this repository's files and nothing else.
- **Keep material and secrets out of the repository.** `.gitignore` covers `node_modules/`, `film_out/`, `build/` and `*.local.json`; screenshots of your own product and any key stay on your machine.

## 中文
### 如何报告问题
请通过本仓库 GitHub 上的 **Security → Report a vulnerability** 页面私下报告漏洞（若看不到该入口，请新建一个只说明"有安全问题要报告"、不写细节的 issue，维护者会安排私下沟通）。修复之前请不要公开利用细节。

### 运行前需要了解
Reelwright 在你自己的电脑上运行，不向任何地方发送数据，也没有遥测。部分功能会有意地运行代码或访问文件：
- **`film.json` 是受信任的输入。** `"scripts"` 和 `"css"` 会在本机 Chromium 里运行（启动时带 `--allow-file-access-from-files`，页面才能读取自己的素材）。只渲染你自己写的、或读过的片子。
- **`record_ui.mjs` 的录制脚本是受信任的输入。** `serve.cmd` 会在你指定的目录里执行你写的命令。录制用的浏览器默认只允许访问本机、使用空白配置，并且只停止它自己启动的服务。
- **`capture_app.mjs` 会启动已安装的应用。** 它把应用的配置复制到临时文件夹（绝不写回原处）；`"profile_extra": ["secrets"]` 还会把加密的密钥库复制过去，只在你要求时才这样做，运行结束后副本会删除。它从不输入密钥或密码。
- **下载步骤是明确的。** 模型和声音只在你同意后获取；安装脚本只复制本仓库的文件。
- **不要把素材和密钥放进仓库。** `.gitignore` 已覆盖 `node_modules/`、`film_out/`、`build/` 和 `*.local.json`；你自己产品的截图和任何密钥都留在本机。
