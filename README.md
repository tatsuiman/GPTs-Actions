# Overview
GPTs specialized in knowledge management.

[日本語](./README_ja.md)
[中文](./README_zh.md)

## Demo
### Execute code in GAS
![](docs/gas-code-interpreter.gif)

[Setup Instructions](. /GAS/code_interpreter/README.md)
### Run the code in Jupyter
![](docs/open-code-interpreter.gif)

[how to set up](https://zenn.dev/tatsui/articles/gpts-actions)
### Slack Search
![](docs/slack.gif)

## Related Articles.
* [I want to run a language other than Python on ChatGPT "Code Interpreter"](https://zenn.dev/tatsui/articles/local-code-interpreter)
* [Jupyter ✖️ Building a ChatGPT self-hosted "Code Interpreter"](https://zenn.dev/tatsui/articles/gpts-actions)

## Functions
Below is a list of functions that can be called by the chatbot, along with the necessary environment variables and authentication information.
For details on how to implement your own functions, [click here](. /src/functions/README.md)

- `jupyter_create_kernel`: Create a remote Jupyter Notebook kernel.
    - `NGROK_API_KEY`.
    - `JUPYTER_TOKEN`.
- `jupyter_execute_code`: Execute code in the remote Jupyter Notebook.
    - `NGROK_API_KEY`
    - `JUPYTER_TOKEN`.
- `jupyter_write_file`: Write a file to the remote Jupyter Notebook.
    - `NGROK_API_KEY`
    - `JUPYTER_TOKEN`.
- `gas_execute_code`: Execute code in Google Apps Script.
    - `GAS_SPREADSHEET_ID`
    - `src/data/service_account.json`.
- `create_notion_page`: Create a Notion page with the given title and content.
    - `NOTION_SECRET`
    - `NOTION_DATABASE_ID`.
- `append_notion_page`: Append the content to the Notion page.
    - `NOTION_SECRET`.
    - `NOTION_DATABASE_ID`.
- `open_youtube_url`: retrieve subtitles from Youtube URL.
- `open_slack_url`: retrieve the message list of a thread from a Slack URL.
    - `SLACK_BOT_TOKEN`.
- `open_notion_url`: retrieve the content of the page using NotionAPI.
    - `NOTION_SECRET`.
- `open_url`: Open the given URL and retrieve its content. Used for web page scraping and API responses.
- `open_slack_canvas_url`: retrieve content from the slack canvas url.
    - `SLACK_BOT_TOKEN`.
    - `SLACK_USER_TOKEN`.
- `google_search`: search for information from the entire web using Google's custom search engine. Returns search results based on specific keywords.
    - `GOOGLE_CSE_ID`.
    - `GOOGLE_API_KEY`.
- `arxiv_search`: searches for articles using arXive.
- `location_search`: Finds the latitude and longitude of an address based on keywords.
- `trend_search`: Performs a Google trend search.
- `youtube_search`: Search Youtube videos.
- `google_drive_search`: Search for file names from Google Drive. Returns search results based on keywords.
    - `src/data/service_account.json`.
- `slack_search`: Search the message history of a specific channel or user using Slack's API.
    - `SLACK_BOT_TOKEN`
    - `SLACK_USER_TOKEN`.
- `notion_search`: Use Notion's API to search pages and databases within Notion.
    - `NOTION_SECRET`.
- `github_search`: Search for Issues, Pull Requests, and code in GitHub and return results.
    - `GITHUB_TOKEN`.
- `get_github_discussion`: allows you to retrieve a list of discussions from a Github Discussion URL.
    - `GITHUB_TOKEN`.
- `fact_checker`: use Google's Fact Check Tools API to investigate the veracity of a particular claim or news item.
    - `GOOGLE_API_KEY`
- `intelx_search`: uses Intelligence X's API to search for information from various data sources (web pages, forums, documents, etc.).
    - `INTELX_API_KEY`
- `ingest_memory`: memorize important content of a conversation.
    - `PINECONE_API_KEY`.
    - `OPENAI_API_KEY`.
- `semantic_search_memory`: search the semantic content of the conversation.
    - `PINECONE_API_KEY`
    - `OPENAI_API_KEY`

## Deploy
```bash
cp env.sample .envrc
direnv allow
npm install -g serverless
serverless plugin install -n serverless-api-gateway-throttling
serverless plugin install -n serverless-prune-plugin
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
sls deploy
```

## Jupyter notebook
```bash
git clone https://github.com/tatsuiman/jupyter-ngrok-worker
cd jupyter-ngrok-worker
cp env.sample .env
vim .env
vim docker/nginx/nginx.conf
docker-compose up -d --build
```

## Create GPTs

GPTs can be set up by reading [here](/openapi/README.md) to set them up.
