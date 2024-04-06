import os
import json
from notion.util import (
    create_notion_page,
    markdown_to_notion_blocks,
    append_blocks_to_page,
)

# NotionデータベースID
DATABASE_ID = os.getenv("DATABASE_ID")


def run(title, content):
    # 新しいページを作成
    properties = {}
    resp = create_notion_page(DATABASE_ID, title, properties)
    try:
        # MarkdownをNotionブロックに変換
        blocks = markdown_to_notion_blocks(content)
        # Notionページにブロックを追加
        id = resp["id"]
        url = resp["url"]
        append_blocks_to_page(id, blocks)
        return json.dumps({"status": "success", "url": url, "page_id": id})
    except:
        return json.dumps({"status": "failed"})
