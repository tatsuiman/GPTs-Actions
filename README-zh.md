# 概览
GPT 专门从事知识管理。

[日本語](./README_ja.md)

### 演示
### 在 GAS 中执行代码
![](docs/gas-code-interpreter.gif)

[设置说明](./GAS/code_interpreter/README-zh.md)
### 在 Jupyter 中运行代码
![](docs/open-code-interpreter.gif)

[如何设置](https://zenn.dev/tatsui/articles/gpts-actions)
### Slack 搜索
![](docs/slack.gif)

## 相关文章。
* [我想在 ChatGPT "代码解释器 "上运行 Python 以外的语言](https://zenn.dev/tatsui/articles/local-code-interpreter)
* [Jupyter ✖️ 构建 ChatGPT 自托管 "代码解释器"](https://zenn.dev/tatsui/articles/gpts-actions)

### 功能
下面列出了聊天机器人可以调用的函数，以及必要的环境变量和身份验证信息。  
有关如何实现自己的函数的详细信息，请 [单击此处](./src/functions/README-zh.md)

- jupyter_create_kernel`：创建远程 Jupyter Notebook 内核。
    - `ngrok_api_key`.
    - jupyter_token`。
- `jupyter_execute_code`：在远程 Jupyter Notebook 中执行代码。
    - `ngrok_api_key`: 在远程 Jupyter 笔记本中执行代码。
    - jupyter_token`。
- jupyter_write_file`：向远程 Jupyter Notebook 写入文件。
    - `ngrok_api_key` `jupyter_token`.
    - jupyter_token`。
- `gas_execute_code`：在 Google Apps 脚本中执行代码。
    - `gas_spreadsheet_id`: 在谷歌应用程序脚本中执行代码。
    - src/data/service_account.json`。
- `create_notion_page`：用给定的标题和内容创建一个 Notion 页面。
    - `notion_secret
    - notion_database_id`。
- `append_notion_page`：将内容添加到 Notion 页面。
    - `notion_secret`.
    - `notion_database_id`.
- `open_youtube_url`: 从 Youtube URL 获取字幕。
- open_slack_url`：从 Slack URL 获取线程的消息列表。
    - `slack_bot_token`.
- open_notion_url`：使用 NotionAPI 获取页面内容。
    - `notion_secret`.
- `open_url`：打开给定的 URL 并获取其内容。用于网页搜刮和 API 响应。
- `open_slack_canvas_url`：从 slack canvas 网址获取内容。
    - `slack_bot_token`.
    - slack_user_token`。
- `google_search`: 使用 Google 的自定义搜索引擎搜索整个网络的信息。根据特定关键词返回搜索结果。
    - `google_cse_id`.
    - google_api_key`。
- arxiv_search`：使用 arXive 搜索文章。
- `location_search`：根据关键字查找地址的经度和纬度。
- `trend_search`：执行 Google 趋势搜索。
- `youtube_search`：搜索 Youtube 视频。
- `google_drive_search`：从 Google Drive 搜索文件名。根据关键字返回搜索结果。
    - src/data/service_account.json`。
- `slack_search`：使用 Slack 的 API 搜索特定频道或用户的消息历史记录。
    - `slack_bot_token`.
    - slack_user_token`。
- `notion_search`：使用 Notion 的 API 搜索 Notion 中的页面和数据库。
    - notion_secret`。
- github_search`：在 GitHub 中搜索问题、Pull Requests 和代码并返回结果。
    - `github_token`.Github_search`：在 GitHub 中搜索问题、拉取请求和代码，并返回结果。
- get_github_discussion`：允许您从 Github 讨论 URL 获取讨论列表。
    - `github_token`.
- fact_checker`：使用 Google 的事实检查工具 API 来调查特定声明或新闻的真实性。
    - `google_api_key`.
- `intelx_search`: 使用 Intelligence X 的 API 从各种数据源（网页、论坛、文档等）中搜索信息。
    - `intelx_api_key`.
- `ingest_memory`: 记忆对话的重要内容。
    - `pinecone_api_key`.
    - `openai_api_key`.
- 语义搜索内存"：搜索对话的语义内容。
    - `pinecone_api_key`.
    - `openai_api_key`.

## 部署
```bash
cp env.sample .envrc
允许
npm install -g serverless
无服务器插件安装 -n serverless-api-gateway-throttling
无服务器插件 install -n serverless-prune-plugin
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
sls 部署
```

## Jupyter 笔记本
```bash
git clone https://github.com/tatsuiman/jupyter-ngrok-worker
cd jupyter-ngrok-worker
cp env.sample .env
vim .env
vim docker/nginx/nginx.conf
docker-compose up -d --build
```

## 创建 GPT

可以通过阅读[此处](./openapi/README-zh.md)来设置 GPT。
