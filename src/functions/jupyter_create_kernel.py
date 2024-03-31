import os
import json
import requests

# Jupyterサーバーの設定
JUPYTER_HOST = os.getenv("JUPYTER_HOST")
TOKEN = os.getenv("JUPYTER_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}


def create_kernel():
    # 新しいカーネルを起動
    response = requests.post(
        f"https://{JUPYTER_HOST}/api/kernels", json={"name": "python3"}, headers=HEADERS
    )
    kernel_id = response.json()["id"]
    print(f"Kernel {kernel_id} started.")

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
        f"https://{JUPYTER_HOST}/api/contents/{kernel_id}.ipynb",
        json=notebook_data,
        headers=HEADERS,
    )
    print(f"Notebook {kernel_id}.ipynb created.")
    return kernel_id


def run():
    kernel_id = create_kernel()
    return json.dumps({"kernel_id": kernel_id})


if __name__ == "__main__":
    print(run())
