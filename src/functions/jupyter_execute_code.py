import os
import json
import uuid
import requests
import websocket
import logging

# Jupyterサーバーの設定
JUPYTER_HOST = os.getenv("JUPYTER_HOST")
TOKEN = os.getenv("JUPYTER_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}


def add_cell(kernel_id, code, outputs):
    # ノートブックの内容を取得
    response = requests.get(
        f"https://{JUPYTER_HOST}/api/contents/{kernel_id}.ipynb", headers=HEADERS
    )
    notebook_data = response.json()["content"]

    # コードセルを追加
    code_cell = {
        "cell_type": "code",
        "execution_count": None,  # 実行回数はJupyterが自動的に管理
        "metadata": {},
        "outputs": outputs,
        "source": code,
    }
    notebook_data["cells"].append(code_cell)

    # ノートブックを更新
    update_response = requests.put(
        f"https://{JUPYTER_HOST}/api/contents/{kernel_id}.ipynb",
        headers=HEADERS,
        data=json.dumps({"content": notebook_data, "type": "notebook"}),
    )
    if update_response.ok:
        print("Notebook updated successfully.")
    else:
        print(update_response.text)
        print("Failed to update notebook.")


def execute_code(code, kernel_id):
    output = ""
    # JupyterサーバーのWebSocket URL
    ws_url = f"wss://{JUPYTER_HOST}/api/kernels/{kernel_id}/channels"
    # WebSocket接続の開始
    ws = websocket.create_connection(ws_url, header=HEADERS)
    try:
        # 実行するコード
        header = {
            "msg_type": "execute_request",
            "msg_id": uuid.uuid1().hex,
            "session": uuid.uuid1().hex,
        }
        message = json.dumps(
            {
                "header": header,
                "parent_header": header,
                "metadata": {},
                "content": {"code": code, "silent": False},
            }
        )
        # 送信
        ws.send(message)
        # 結果の保持
        outputs = []
        while True:
            response = json.loads(ws.recv())
            msg_type = response["msg_type"]

            if msg_type == "error":
                for error in response["content"]["traceback"]:
                    outputs.append(
                        {"output_type": "stream", "name": "stdout", "text": error}
                    )
                    output += error

            if msg_type == "stream":
                text = response["content"]["text"]
                outputs.append(
                    {"output_type": "stream", "name": "stdout", "text": text}
                )
                output += text

            if msg_type == "display_data":
                imgdata = response["content"]["data"]
                outputs.append(
                    {
                        "output_type": "display_data",
                        "data": {
                            "text/plain": [imgdata["text/plain"]],
                            "image/png": imgdata["image/png"],
                        },
                        "metadata": {},
                    }
                )

            if msg_type == "execute_reply":
                break
        add_cell(kernel_id, code, outputs)
    finally:
        ws.close()
    return output


def run(code, kernel_id):
    try:
        output = execute_code(code, kernel_id)
        return output
    except Exception as e:
        logging.exception(e)
        return "カーネルが起動していません。もう一度カーネルを作成してください。"


if __name__ == "__main__":
    import sys

    kernel_id = sys.argv[1]
    print(run("print('Hello, World!')", kernel_id))
