# 概要
ナレッジ管理に特化したGPTsです。

## Demo
### GASでコードを実行
![](docs/gas-code-interpreter.gif)

[セットアップ方法](./GAS/code_interpreter/README.md)
### Jupyterでコードを実行
![](docs/open-code-interpreter.gif)

[セットアップ方法](https://zenn.dev/tatsui/articles/gpts-actions)
### Slack検索
![](docs/slack.gif)

## 関連記事
* [ChatGPT「Code Interpreter」でPython以外の言語を動かしたい](https://zenn.dev/tatsui/articles/local-code-interpreter)
* [Jupyter ✖️ ChatGPT セルフホストの「Code Interpreter」を構築する](https://zenn.dev/tatsui/articles/gpts-actions)

## Functions
以下はチャットボットが呼び出し可能な機能と必要な環境変数や認証情報の一覧です。
独自のfunctionの実装方法は[こちら](./src/scripts/functions/README.md)

- `jupyter_create_kernel`: リモートのJupyter Notebook のカーネルを作成する。
    - `NGROK_API_KEY`
    - `JUPYTER_TOKEN`
- `jupyter_execute_code`: リモートのJupyter Notebook でコードを実行する。
    - `NGROK_API_KEY`
    - `JUPYTER_TOKEN`
- `jupyter_write_file`: リモートのJupyter Notebook にファイルを書き込む
    - `NGROK_API_KEY`
    - `JUPYTER_TOKEN`
- `gas_execute_code`: Google Apps Script でコードを実行します。
    - `GAS_SPREADSHEET_ID`
    - `src/data/service_account.json`
- `create_notion_page`: 指定されたタイトルと内容でNotionページを作成します。
    - `NOTION_SECRET`
    - `NOTION_DATABASE_ID`
- `append_notion_page`: Notionページに内容を追加します。
    - `NOTION_SECRET`
    - `NOTION_DATABASE_ID`
- `open_youtube_url`: YoutubeのURLから字幕を取得します。
- `open_slack_url`: SlackのURLからスレッドのメッセージ一覧を取得します。
    - `SLACK_BOT_TOKEN`
- `open_notion_url`: NotionAPIを利用してしページの内容を取得します。
    - `NOTION_SECRET`
- `open_url`: 指定されたURLを開き、その内容を取得します。ウェブページのスクレイピングやAPIのレスポンス取得に使用されます。
- `open_slack_canvas_url`: slack canvas urlからコンテンツを取得します。
    - `SLACK_BOT_TOKEN`
    - `SLACK_USER_TOKEN`
- `google_search`: Googleのカスタム検索エンジンを利用して、ウェブ全体から情報を検索します。特定のキーワードに基づいた検索結果を返します。
    - `GOOGLE_CSE_ID`
    - `GOOGLE_API_KEY`
- `arxiv_search`: arXiveを使って論文を検索します。
- `location_search`: キーワードから住所の緯度経度を求めます。
- `trend_search`: Googleトレンド検索を行います。
- `youtube_search`: Youtubeの動画を検索します。
- `google_drive_search`: Google Driveからファイル名を検索することができます。キーワードに基づいた検索結果を返します。
    - `src/data/service_account.json`
- `slack_search`: SlackのAPIを利用して、特定のチャンネルやユーザーのメッセージ履歴を検索します。
    - `SLACK_BOT_TOKEN`
    - `SLACK_USER_TOKEN`
- `notion_search`: NotionのAPIを利用して、Notion内のページやデータベースを検索します。
    - `NOTION_SECRET`
- `github_search`: GitHub内でのIssue、Pull Request、コードの検索を行い、結果を返します。
    - `GITHUB_TOKEN`
- `get_github_discussion`: Github DiscussionのURLからディスカッション一覧を取得することができます。
    - `GITHUB_TOKEN`
- `fact_checker`: GoogleのFact Check Tools APIを利用して、特定の主張やニュースの真偽を調査します。
    - `GOOGLE_API_KEY`
- `intelx_search`: Intelligence XのAPIを利用して、様々なデータソース（ウェブページ、フォーラム、ドキュメントなど）から情報を検索します。
    - `INTELX_API_KEY`
- `ingest_memory`: 会話の重要な内容を記憶します。
    - `PINECONE_API_KEY`
    - `OPENAI_API_KEY`
- `semantic_search_memory`: 会話の重要な内容を検索します。
    - `PINECONE_API_KEY`
    - `OPENAI_API_KEY`

## デプロイ
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
