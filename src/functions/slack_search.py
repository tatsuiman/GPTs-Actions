import os
import json
import logging
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def run(keyword: str, user_token: str) -> str:
    """Slackのメッセージと関連情報を検索できます。検索キーワードとなる日本語の文字列を入力してください。"""

    # Slackクライアントの初期化
    client = WebClient(token=user_token)

    try:
        # メッセージを検索
        resp = client.search_messages(query=keyword)

        # 検索結果を返す
        if resp.status_code == 200:
            messages = ""
            if resp["ok"]:
                for message in resp["messages"]["matches"]:
                    # プライベートメッセージは除外する
                    if (
                        message["type"] == "message"
                        and message["channel"]["is_private"] == False
                        and message["channel"]["is_mpim"] == False
                        and message["channel"]["is_group"] == False
                        and message["channel"]["is_im"] == False
                    ):
                        logging.debug(f'{message["permalink"]}\n')
                        timestamp = float(message["ts"])
                        dt_object = datetime.fromtimestamp(timestamp)
                        messages += f"[{dt_object.isoformat()}] <@{message['user']}>: {message['text']}\n"
                # レスポンスの作成
                return (
                    f"#チャット履歴\n{messages}\n---\n"
                    "※ チャット履歴にURLが含まれる場合は別のツールで開いてください。"
                )
            else:
                return resp["error"]

    except SlackApiError as e:
        # エラーが発生した場合
        return f"Error searching messages: {str(e)}"
    return "Slackの検索結果は何も見つかりませんでした。"
