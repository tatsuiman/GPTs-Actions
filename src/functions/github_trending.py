import json
import re
import urllib.parse
import bs4
import requests


def run(language, since):
    url = f"https://github.com/trending/{language}?since={since}"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "lxml")
    html_content = soup.prettify()
    # Regular expression to find repository paths
    pattern = re.compile(r"href=\"/([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)\"")
    matches = pattern.findall(html_content)
    repo_names = [urllib.parse.unquote(match) for match in matches]
    # Further filter to avoid links to GitHub features or sponsor pages
    filtered_repo_names = [
        name
        for name in repo_names
        if not any(
            keyword in name
            for keyword in ["features", "sponsors", "enterprise", "apps", "trending"]
        )
    ]
    unique_repo_names = list(set(filtered_repo_names))  # Remove duplicates
    return json.dumps({"repo_names": unique_repo_names}, ensure_ascii=False)


if __name__ == "__main__":
    print(run("", "daily"))
