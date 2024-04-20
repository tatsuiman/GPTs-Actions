import os
import logging
from jupyter_api import JupyterClient
from tools import get_ngrok_public_host


def run(
    command,
    jupyter_token=os.getenv("JUPYTER_TOKEN"),
    ngrok_api_key=os.getenv("NGROK_API_KEY"),
):
    try:
        JUPYTER_HOST = (
            os.getenv("JUPYTER_HOST")
            if len(os.getenv("JUPYTER_HOST", "")) > 0
            else get_ngrok_public_host(ngrok_api_key)
        )
        SCHEMA = os.getenv("SCHEMA", "https")
        client = JupyterClient(JUPYTER_HOST, SCHEMA, jupyter_token)
        # コマンド実行はpythonしか対応していない
        kernel_id = client.create_kernel(language="python3")
        output = client.execute_code(f"!{command}", kernel_id, cell=False)
        client.delete_kernel(kernel_id)
        return output
    except Exception as e:
        logging.exception(e)
        return "コマンドの実行に失敗しました。"


if __name__ == "__main__":
    import sys

    kernel_id = sys.argv[1]
    r = run("ls -l")
    print(r)
