import os
import json
from notion.util import (
    markdown_to_notion_blocks,
    append_blocks_to_page,
)

# NotionデータベースID
DATABASE_ID = os.getenv("DATABASE_ID")


def run(page_id, content):
    try:
        # MarkdownをNotionブロックに変換
        blocks = markdown_to_notion_blocks(content)
        append_blocks_to_page(page_id, blocks)
        return json.dumps({"status": "success"})
    except:
        return json.dumps({"status": "failed"})
