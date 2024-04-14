import re
import os
import json
import requests
from tempfile import mkdtemp
from tools import browser_open

IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")


# テキストからHTMLスクリプトを抽出し、PNGファイルとして保存する関数
def run(script):
    # 一時HTMLファイルのパスを生成
    html_file = os.path.join(mkdtemp(), "output.html")
    with open(html_file, "w") as f:
        f.write(script)
    # ファイルのURLを生成
    url = "file://" + os.path.abspath(html_file)
    # 出力PNGファイルのパスを生成
    png_file = os.path.join(mkdtemp(), "html.png")
    # ブラウザを開いてPNGファイルを生成
    browser_open(url, png_file)
    # upload imgur
    headers = {
        "authorization": f"Client-ID {IMGUR_CLIENT_ID}",
    }
    files = {
        "image": (open(png_file, "rb")),
    }
    r = requests.post("https://api.imgur.com/3/upload", headers=headers, files=files)
    return json.dumps({"imgur_url": f"![[{r.json()['data']['link']}]]"})
