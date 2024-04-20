import os
import json
from notion.util import Notion, markdown_to_notion_blocks


def run(page_id, content, notion_secret):
    try:
        # MarkdownをNotionブロックに変換
        notion = Notion(notion_secret)
        blocks = markdown_to_notion_blocks(content)
        notion.append_blocks_to_page(page_id, blocks)
        return json.dumps({"status": "success"})
    except:
        return json.dumps({"status": "failed"})
