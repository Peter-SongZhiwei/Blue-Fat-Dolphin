# 蓝色大肥鱼 · Blue Fat Dolphin

显示 GIF 动图，点击 **API KEY** 后输入公司缩写，通过服务端验证后查看内容。`zte` 大小写不敏感，也会忽略两端空格。关闭弹窗后清空显示内容，每次查看重新验证。

## 部署到 Vercel

1. 在 Vercel 导入此 GitHub 仓库。
2. Framework Preset 选择 **Other**，保留默认构建设置，不需要安装依赖或构建命令。
3. 在项目 **Settings → Environment Variables** 添加服务端变量 `API_KEY`，值填入需要展示的完整内容。勾选需要的环境（至少 Production）。不要使用公开前缀或把密钥放进 HTML。
4. 点击 Deploy。修改环境变量后重新部署。
5. 打开部署网址，点击 **API KEY**，输入公司缩写后查看。输入错误应提示失败；未配置环境变量时提示管理员配置。

线上接口 `api/key.py` 从 Vercel 环境变量读取内容，无法访问电脑上的 `~/dev/API_KEY`。接口只允许 POST 获取密钥，响应不缓存。公司缩写是简单的共享口令，知道缩写的人均可查看完整内容。

参考：[Vercel Python 接口](https://vercel.com/docs/functions/runtimes/python/api-directory)、[环境变量](https://vercel.com/docs/environment-variables)。

## 本地运行

需要 Python 3，无额外依赖：

```sh
cd ~/dev/gif-page
python3 server.py
```

浏览器打开 http://127.0.0.1:8765 。端口被占用时可用 `python3 server.py --port 8766`。

本地服务读取 `~/dev/API_KEY`，仅监听本机。直接双击 HTML 无法读取文件。`server.py` 供本地使用，不上传到 Vercel 部署产物。

## 文件

- `index.html`：页面、验证输入框与密钥弹窗。
- `fish.gif`：原始 GIF 动图。
- `api/key.py`：Vercel 服务端验证与环境变量读取。
- `server.py`：本地预览与文件读取。
- `vercel.json`：Vercel 项目设置与响应头。

真实密钥、`.env` 和 Vercel 本地配置已列入忽略规则，不应提交到仓库。
