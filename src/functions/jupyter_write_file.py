import os
import sys
from jupyter_api import JupyterClient
from tools import get_ngrok_public_host
from tempfile import mkdtemp


def run(
    content,
    file_path,
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
    temp_file_path = os.path.join(mkdtemp(), "temp.txt")
    with open(temp_file_path, "w") as f:
        f.write(content)
    return client.upload_file(temp_file_path, file_path)


if __name__ == "__main__":
    print(run(sys.argv[1], sys.argv[2]))
