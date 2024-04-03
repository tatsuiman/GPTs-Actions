import json
import urllib.parse


def run(keywords):
    keywords = keywords.split(",")
    comma_encoded_keywords = urllib.parse.quote(",".join(keywords))
    space_encoded_keywords = urllib.parse.quote(" ".join(keywords))
    google_trends_url = (
        f"https://trends.google.co.jp/trends/explore?q={comma_encoded_keywords}&hl=ja"
    )
    google_search_url = f"https://www.google.co.jp/search?q={space_encoded_keywords}"
    youtube_search_url = (
        f"https://www.youtube.com/results?search_query={space_encoded_keywords}"
    )
    twitter_search_url = (
        f"https://twitter.com/search?q={space_encoded_keywords}&src=typed_query"
    )
    reddit_search_url = f"https://www.reddit.com/search/?q={space_encoded_keywords}"
    twoch_search_url = f"https://find.5ch.net/search?q={space_encoded_keywords}"
    return json.dumps(
        {
            "google_trends_url": google_trends_url,
            "google_search_url": google_search_url,
            "youtube_search_url": youtube_search_url,
            "twitter_search_url": twitter_search_url,
            "reddit_search_url": reddit_search_url,
            "twoch_search_url": twoch_search_url,
        },
        ensure_ascii=False,
        indent=4,
    )
