import json
import os
from jupyter_api import JupyterClient
from tools import get_ngrok_public_host


def run(
    language,
    jupyter_token=os.getenv("JUPYTER_TOKEN"),
    ngrok_api_key=os.getenv("NGROK_API_KEY"),
):
    JUPYTER_HOST = (
        os.getenv("JUPYTER_HOST")
        if len(os.getenv("JUPYTER_HOST", "")) > 0
        else get_ngrok_public_host(ngrok_api_key)
    )
    SCHEMA = os.getenv("SCHEMA", "https")
    client = JupyterClient(JUPYTER_HOST, SCHEMA, jupyter_token)
    kernel_id = client.create_kernel(language)
    return json.dumps({"kernel_id": kernel_id})


if __name__ == "__main__":
    import sys

    print(run(sys.argv[1]))
