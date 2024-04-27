import logging
from notion.util import Notion
from timeout_decorator import timeout, TimeoutError


@timeout(20)
def open_url(url, notion, recursive=True):
    return notion.get_page_markdown(url, recursive=recursive)


def run(url, notion_secret):
    notion = Notion(notion_secret)
    try:
        return open_url(url, notion, recursive=True)
    except TimeoutError:
        return "TimeoutError:コンテンツが大きすぎます"
