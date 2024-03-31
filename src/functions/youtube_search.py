import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# サービスアカウントの情報を読み込む
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
SERVICE_ACCOUNT_FILE = "../data/service_account.json"


def run(keyword):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    # YouTube APIクライアントを構築
    youtube = build("youtube", "v3", credentials=credentials)

    # 検索キーワードを設定

    # YouTubeで動画を検索し、動画のみを対象にフィルタリング
    search_response = (
        youtube.search()
        .list(
            q=keyword,
            part="snippet",
            maxResults=5,
            type="video",  # 動画のみを対象にフィルタリング
        )
        .execute()
    )

    # 検索結果を表示
    results = []
    for item in search_response.get("items", []):
        results.append(
            {
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "channelTitle": item["snippet"]["channelTitle"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            }
        )
    return json.dumps(results, ensure_ascii=False)
