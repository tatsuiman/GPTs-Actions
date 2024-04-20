import os
import logging
from googleapiclient.discovery import build

# https://note.com/npaka/n/nd9a4a26a8932


def run(
    keyword,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    google_cse_id=os.getenv("GOOGLE_CSE_ID"),
):
    # Google Search APIを使って各キーワードを検索
    service = build("customsearch", "v1", developerKey=google_api_key)
    results = ""
    res = service.cse().list(q=keyword, cx=google_cse_id).execute()
    items = list(res.get("items", []))
    logging.info(f"hit {len(items)} urls")
    for item in items:
        # print(item)
        results += f'* title: "{item["title"]}"\n'
        results += f'  - snippet: `{item["snippet"]}`\n'
        results += f'  - url: "{item["formattedUrl"]}"\n\n'
    return results
