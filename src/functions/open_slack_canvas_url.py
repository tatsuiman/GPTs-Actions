import re
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from slacklib import SlackClient


def extract_slack_canvas_url(url, bot_token):
    messages = ""
    slack_client = SlackClient(bot_token=bot_token)
    try:
        # URLからチャンネルIDを抽出
        url_pattern = r"slack\.com/canvas/([A-Z0-9]+)"
        matches = re.findall(url_pattern, url)
        for channel_id in matches:
            if channel_id:
                messages = slack_client.get_canvas_content(channel_id)
            else:
                messages = "URLが不正です。"
    except Exception as e:
        messages = f"Failed to extract slack url: {str(e)}"
    return messages


def run(url, bot_token, user_token):
    canvas_content = extract_slack_canvas_url(url, bot_token, user_token)
    return canvas_content
