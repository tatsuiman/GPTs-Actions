import logging
from notion.util import Notion


def run(url, notion_secret):
    notion = Notion(notion_secret)
    page_content = notion.get_page_markdown(url, recursive=True)
    return page_content
