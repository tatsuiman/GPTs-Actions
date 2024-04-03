import os
import json
import uuid
import requests
import websocket
import logging
from tools import get_ngrok_public_host

JUPYTER_HOST = (
    os.getenv("JUPYTER_HOST")
    if len(os.getenv("JUPYTER_HOST")) > 0
    else get_ngrok_public_host()
)
SCHEMA = os.getenv("SCHEMA", "https")
TOKEN = os.getenv("JUPYTER_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}
SCHEMA = os.getenv("SCHEMA", "https")
WS_SCHEMA = "wss" if SCHEMA == "https" else "ws"


def create_kernel(language="python3"):
    try:
        response = requests.get(
            f"{SCHEMA}://{JUPYTER_HOST}/api/kernelspecs",
            headers=HEADERS,
        )
        kernelspecs = response.json()["kernelspecs"]
        supported_kenellist = list(kernelspecs.keys())
        logging.info(supported_kenellist)
        if language not in supported_kenellist:
            return f"{language} is not supported. (supported kernels: {supported_kenellist})"
    except Exception as e:
        return e

    try:
        # 新しいカーネルを起動
        response = requests.post(
            f"{SCHEMA}://{JUPYTER_HOST}/api/kernels",
            json={"name": language},
            headers=HEADERS,
        )
        response.raise_for_status()  # エラーがあればここで例外を発生させる
        resp = response.json()
        kernel_id = resp["id"]
        logging.info(f"Kernel {kernel_id} started.")

        notebook_data = {
            "type": "notebook",
            "content": {
                "cells": [],
                "metadata": {},
                "nbformat": 4,
                "nbformat_minor": 2,
            },
        }
        response = requests.put(
            f"{SCHEMA}://{JUPYTER_HOST}/api/contents/{kernel_id}.ipynb",
            json=notebook_data,
            headers=HEADERS,
        )
        response.raise_for_status()  # エラーがあればここで例外を発生させる
        logging.info(f"Notebook {kernel_id}.ipynb created.")
        return kernel_id
    except requests.exceptions.RequestException as e:
        return f"カーネルの作成またはノートブックの作成中にエラーが発生しました: {e}"


def delete_kernel(kernel_id):
    response = requests.delete(
        f"{SCHEMA}://{JUPYTER_HOST}/api/kernels/{kernel_id}", headers=HEADERS
    )
    if response.ok:
        logging.info(f"Kernel {kernel_id} deleted.")
    else:
        logging.error(f"Failed to delete kernel {kernel_id}.")


def add_cell(kernel_id, code, outputs):
    # ノートブックの内容を取得
    response = requests.get(
        f"{SCHEMA}://{JUPYTER_HOST}/api/contents/{kernel_id}.ipynb", headers=HEADERS
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
        f"{SCHEMA}://{JUPYTER_HOST}/api/contents/{kernel_id}.ipynb",
        headers=HEADERS,
        data=json.dumps({"content": notebook_data, "type": "notebook"}),
    )
    if update_response.ok:
        logging.info("Notebook updated successfully.")
    else:
        logging.error(update_response.text)
        logging.error("Failed to update notebook.")


def execute_code(code, kernel_id, timeout=20, cell=True):
    output = ""
    outputs = []
    execute_reply = False
    # JupyterサーバーのWebSocket URL
    session_id = uuid.uuid1().hex
    ws_url = f"{WS_SCHEMA}://{JUPYTER_HOST}/api/kernels/{kernel_id}/channels?session_id={session_id}"
    # WebSocket接続の開始
    ws = websocket.create_connection(ws_url, header=HEADERS, timeout=timeout)
    try:
        # 実行するコード
        header = {
            "msg_type": "execute_request",
            "msg_id": uuid.uuid1().hex,
            "session": session_id,
            "username": "",
        }
        message = json.dumps(
            {
                "header": header,
                "parent_header": header,
                "metadata": {},
                "content": {
                    "code": code,
                    "silent": False,
                    "store_history": True,
                    "stop_on_error": True,
                    "allow_stdin": True,
                    "user_expressions": {},
                },
            }
        )
        # 送信
        ws.send(message)
        # 結果の保持
        while True:
            response = json.loads(ws.recv())
            msg_type = response["msg_type"]
            # print(msg_type)
            # print(json.dumps(response, indent=4))

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
                if execute_reply:
                    break

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
                execute_reply = True

            if msg_type == "status":
                if response["content"]["execution_state"] == "idle" and execute_reply:
                    break
                if response["content"]["execution_state"] == "restarting":
                    break

    except websocket._exceptions.WebSocketTimeoutException:
        pass
    finally:
        if cell:
            add_cell(kernel_id, code, outputs)
        ws.close()
    return output
