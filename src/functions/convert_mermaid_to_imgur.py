import re
import os
import json
import requests
from tempfile import mkdtemp
from tools import browser_open

IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")


def mermaid_to_image(mermaid_script):
    png_file = os.path.join(mkdtemp(), "mermaid.png")
    # HTMLテンプレートを生成
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Mermaid</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad:true}});</script>
</head>
<body>
    <div class="mermaid">
    {mermaid_script}
    </div>
</body>
</html>
"""
    # HTMLファイルを保存
    html_file = f"{mkdtemp()}_mermaid_chart.html"
    with open(html_file, "w") as file:
        file.write(html_template)

    url = "file://" + os.path.abspath(html_file)
    content = browser_open(url, png_file)
    return png_file


# convert mermaid to imgur
def run(script):
    png_file = mermaid_to_image(script)
    # upload imgur
    headers = {
        "authorization": f"Client-ID {IMGUR_CLIENT_ID}",
    }
    files = {
        "image": (open(png_file, "rb")),
    }
    r = requests.post("https://api.imgur.com/3/upload", headers=headers, files=files)
    return json.dumps({"imgur_url": f"![[{r.json()['data']['link']}]]"})
