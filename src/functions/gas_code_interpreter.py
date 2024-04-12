import os
import time
import gspread
from uuid import uuid4
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = "data/service_account.json"
SPREADSHEET_ID = os.environ.get("GAS_SPREADSHEET_ID")
SHEET_NAME = os.environ.get("GAS_SHEET_NAME", "Sheet1")


def run(title, code):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    # GCPからダウンロードした認証用のjson
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=scope
    )
    # 認証情報を取得
    gc = gspread.authorize(credentials)

    wb = gc.open_by_key(SPREADSHEET_ID)
    ws = wb.worksheet(SHEET_NAME)
    # 挿入するデータ
    run_id = uuid4().hex
    insert_data = [run_id, title, code]
    # スプレッドシートの最終行にデータを追加
    ws.append_row(insert_data)
    # シートの変更をトリガーにセルのコードがGoogle Apps Scriptで実行され、実行結果の列が更新される
    # 上記で挿入したrun_idと同じ行が更新されるまで1秒ごとにポーリングする
    while True:
        # スプレッドシートのデータを取得
        records = ws.get_all_records()
        for record in reversed(records):
            if record["ID"] == run_id and record["成否"] != "":
                return f"実行結果: {record['実行結果']}"
        else:
            time.sleep(1)
            continue


if __name__ == "__main__":
    run("test", "return 'hoge'")
