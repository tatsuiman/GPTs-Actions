import os
import json
import logging
from notion.util import Notion
from notion_client import Client


def run(keyword: str, notion_secret: str) -> str:
    """Notionのページを検索し、その内容を返します。キーワードを入力してください。"""

    try:
        notion_util = Notion(notion_secret)
        notion_client = Client(auth=notion_secret)
        # キーワードからページのURLを検索
        search_results = notion_client.search(
            query=keyword,
            sort={"direction": "descending", "timestamp": "last_edited_time"},
            page_size=5,
        )
        if not search_results["results"]:
            return "Notionの検索結果は何も見つかりませんでした。"

        # 検索結果を作成
        res = ""
        for result in search_results["results"][:5]:
            if result["object"] != "page":
                continue
            try:
                page_url = result["url"]
                logging.info(f"ページURL: {page_url}")
                # ページの内容を取得
                page_content = notion_util.get_page_markdown(page_url, recursive=False)
                # レスポンスの作成
                res += f"# {page_url}の内容\n{page_content}\n"
            except Exception as e:
                logging.error(f"ページURLの取得に失敗しました: {str(e)}")
                continue

        return res

    except Exception as e:
        # エラーが発生した場合
        return f"エラーが発生しました: {str(e)}"
