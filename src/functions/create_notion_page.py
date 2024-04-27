import os
import json
from notion.util import Notion, markdown_to_notion_blocks


def run(title, content, notion_secret, database_id):
    # 新しいページを作成
    properties = {}
    notion = Notion(notion_secret)
    resp = notion.create_notion_page(database_id, title, properties)
    try:
        # MarkdownをNotionブロックに変換
        blocks = markdown_to_notion_blocks(content)
        # Notionページにブロックを追加
        id = resp["id"]
        url = resp["url"]
        notion.append_blocks_to_page(id, blocks)
        return json.dumps({"status": "success", "url": url, "page_id": id})
    except:
        return json.dumps({"status": "failed"})
