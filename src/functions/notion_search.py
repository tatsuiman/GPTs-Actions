import os
import json
import logging
from notion_client import Client


def run(keyword: str, notion_secret: str) -> str:
    """Notionのページを検索し、その内容を返します。キーワードを入力してください。"""

    try:
        notion_client = Client(auth=notion_secret)
        page_urls = []
        # キーワードからページのURLを検索
        search_results = notion_client.search(
            query=keyword,
            sort={"direction": "descending", "timestamp": "last_edited_time"},
            page_size=20,
        )
        if not search_results["results"]:
            return "Notionの検索結果は何も見つかりませんでした。"

        # 検索結果を作成
        for result in search_results["results"][:5]:
            if result["object"] != "page":
                continue
            page_url = result["url"]
            properties = result["properties"]
            logging.info(f"{page_url}")
            page_urls.append({"url": page_url, "properties": properties})
        return json.dumps({"page_urls": page_urls})

    except Exception as e:
        # エラーが発生した場合
        return f"エラーが発生しました: {str(e)}"
