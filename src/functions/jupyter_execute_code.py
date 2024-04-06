import os
import logging
from jupyter_api import JupyterClient
from tools import get_ngrok_public_host


def run(code, kernel_id):
    try:
        JUPYTER_HOST = (
            os.getenv("JUPYTER_HOST")
            if len(os.getenv("JUPYTER_HOST")) > 0
            else get_ngrok_public_host()
        )
        TOKEN = os.getenv("JUPYTER_TOKEN")
        SCHEMA = os.getenv("SCHEMA", "https")
        client = JupyterClient(JUPYTER_HOST, SCHEMA, TOKEN)
        output = client.execute_code(code, kernel_id)
        return output
    except Exception as e:
        logging.exception(e)
        return (
            f"カーネルが起動していません。もう一度カーネルを作成してください。{str(e)}"
        )


if __name__ == "__main__":
    import sys

    kernel_id = sys.argv[1]
    golang_code = """
import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	resp, err := http.Get("https://api.ipify.org")
	if err != nil {
		fmt.Println("Failed to get IP:", err)
		return
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Failed to read response body:", err)
		return
	}

	fmt.Println("Your Global IP is:", string(body))
}
"""
    js_code = """
fetch('https://api.ipify.org?format=json')
  .then(response => response.json())
  .then(data => console.log(data));

"""
    r = run(golang_code, kernel_id)
    print(r)
