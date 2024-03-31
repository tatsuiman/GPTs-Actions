# 概要
ナレッジ管理に特化したGPTsです。

## Demo
### Slack検索
![](docs/slack.gif)
### コードの実行
![](docs/open-code-interpreter.gif)

## Functions
以下はチャットボットが呼び出し可能な機能一覧です。
独自のfunctionの実装方法は[こちら](./src/scripts/functions/README.md)

- `create_notion_page`: 指定されたタイトルと内容でNotionページを作成します。
- `open_youtube_url`: YoutubeのURLから字幕を取得します。
- `open_slack_url`: SlackのURLからスレッドのメッセージ一覧を取得します。
- `open_notion_url`: NotionAPIを利用してしページの内容を取得します。
- `open_url`: 指定されたURLを開き、その内容を取得します。ウェブページのスクレイピングやAPIのレスポンス取得に使用されます。
- `open_slack_canvas_url`: slack canvas urlからコンテンツを取得します。
- `google_search`: Googleのカスタム検索エンジンを利用して、ウェブ全体から情報を検索します。特定のキーワードに基づいた検索結果を返します。
- `google_drive_search`: Google Driveからファイル名を検索することができます。キーワードに基づいた検索結果を返します。
- `slack_search`: SlackのAPIを利用して、特定のチャンネルやユーザーのメッセージ履歴を検索します。
- `notion_search`: NotionのAPIを利用して、Notion内のページやデータベースを検索します。
- `github_search`: GitHub内でのIssue、Pull Request、コードの検索を行い、結果を返します。
- `get_github_discussion`: Github DiscussionのURLからディスカッション一覧を取得することができます。
- `fact_checker`: GoogleのFact Check Tools APIを利用して、特定の主張やニュースの真偽を調査します。
- `intelx_search`: Intelligence XのAPIを利用して、様々なデータソース（ウェブページ、フォーラム、ドキュメントなど）から情報を検索します。
