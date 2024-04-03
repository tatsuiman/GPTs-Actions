import os
import re
import time
import ngrok
import logging
from bs4 import BeautifulSoup
from selenium import webdriver


def get_ngrok_public_host():
    ngrok_host = ""
    # construct the api client
    client = ngrok.Client(os.getenv("NGROK_API_KEY"))

    # list all online tunnels
    for t in client.tunnels.list():
        if t.forwards_to == "http://nginx:80":
            ngrok_host = t.public_url.replace("https://", "")
    return ngrok_host


def browser_open(url, screenshot_png=None):
    content = ""
    page_source = ""
    title = ""
    WEBDRIVER_TIMEOUT = 10
    WEBDRIVER_ARGUMENTS = (
        "--headless",
        "--no-sandbox",
        "--single-process",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-extensions",
        "--disk-cache-size=0",
        "--aggressive-cache-discard",
        "--disable-notifications",
        "--disable-remote-fonts",
        "--window-size=1366,768",
        "--hide-scrollbars",
        "--disable-audio-output",
    )
    try:
        # Selenium WebDriverの設定
        options = webdriver.ChromeOptions()
        service = webdriver.ChromeService("/opt/chromedriver-linux64/chromedriver")
        options.binary_location = "/opt/chrome-linux64/chrome"

        for opt in WEBDRIVER_ARGUMENTS:
            options.add_argument(opt)

        driver = webdriver.Chrome(options=options, service=service)
        driver.set_page_load_timeout(WEBDRIVER_TIMEOUT)

        # HTMLファイルを開く
        driver.get(url)
        time.sleep(10)  # レンダリングに時間を与える

        # ページのコンテンツを取得
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        # scriptやstyle及びその他タグの除去
        for s in soup(["script", "style"]):
            s.decompose()
        title = soup.title.string if soup.title else "タイトルなし"
        content = soup.get_text()
        content = re.sub(r"\n+", "\n", content)

        # スクリーンショットを保存
        if screenshot_png is not None:
            driver.save_screenshot(screenshot_png)

        # ブラウザを閉じる
        driver.quit()
    except Exception as e:
        logging.error(e)

    return title, content
