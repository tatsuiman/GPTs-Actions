import os
import re
import logging
import requests
from bs4 import BeautifulSoup
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackClient:
    def __init__(
        self,
        bot_token=os.getenv("SLACK_BOT_TOKEN"),
        user_token=os.getenv("SLACK_USER_TOKEN"),
    ):
        self.slack_user_token = user_token
        self.slack_bot_client = WebClient(token=bot_token, timeout=300)

    def get_thread_messages(self, channel_id, thread_ts):
        # すべてのメッセージを保持するリスト
        all_messages = []

        try:
            # 最初のAPIリクエスト
            response = self.slack_bot_client.conversations_replies(
                channel=channel_id, ts=thread_ts
            )

            while True:
                # スレッドのメッセージを取得
                messages = response.get("messages", [])
                all_messages.extend(messages)

                # ページネーションチェック
                response_metadata = response.get("response_metadata", {})
                next_cursor = response_metadata.get("next_cursor")
                if not next_cursor:
                    break  # 最後のページならループを抜ける

                # 次のページのリクエスト
                response = self.slack_bot_client.conversations_replies(
                    channel=channel_id, ts=thread_ts, cursor=next_cursor
                )

        except SlackApiError as e:
            logging.error(
                f"Error fetching conversations: {e} , channel: {channel_id}, ts: {thread_ts}"
            )

        return all_messages

    def get_canvas_content(self, channel_id):
        try:
            # チャンネルの情報を取得
            canvas_content = ""
            response = self.slack_bot_client.conversations_info(channel=channel_id)
            channel_info = response["channel"]
            canvas = channel_info.get("properties", {}).get("canvas", {})
            if canvas.get("is_empty", True) == False:
                file_id = canvas["file_id"]
                # file_idを使ってcanvasをダウンロード
                file_response = self.slack_bot_client.api_call(
                    api_method="files.info", http_verb="GET", params={"file": file_id}
                )
                if file_response["ok"]:
                    file_content = requests.get(
                        file_response["file"]["url_private"],
                        headers={
                            "Authorization": f"Bearer {self.slack_bot_client.token}"
                        },
                    ).content
                    # HTMLのリストアイテムをMarkdownのリストアイテムに変換
                    soup = BeautifulSoup(file_content, "html.parser")
                    for li in soup.find_all("li"):
                        li.replace_with(f"* {li.text}")
                    # HTMLの見出しをMarkdownの見出しに変換
                    for h1 in soup.find_all("h1"):
                        h1.replace_with(f"# {h1.text}")
                    for h2 in soup.find_all("h2"):
                        h2.replace_with(f"## {h2.text}")
                    for h3 in soup.find_all("h3"):
                        h3.replace_with(f"### {h3.text}")
                    for ol in soup.find_all("ol"):
                        for i, li in enumerate(ol.find_all("li")):
                            li.replace_with(f"{i+1}. {li.text}")
                    for ul in soup.find_all("ul"):
                        for li in ul.find_all("li"):
                            li.replace_with(f"* {li.text}")
                    canvas_content = soup.get_text().strip()
        except SlackApiError as e:
            logging.info(f"Error fetching conversation info: {e}")
        return canvas_content
