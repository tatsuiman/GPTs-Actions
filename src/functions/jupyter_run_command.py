import logging
from jupyter_client import create_kernel, execute_code, delete_kernel


def run(command):
    try:
        # コマンド実行はpythonしか対応していない
        kernel_id = create_kernel(language="python3")
        output = execute_code(f"!{command}", kernel_id, cell=False)
        delete_kernel(kernel_id)
        return output
    except Exception as e:
        logging.exception(e)
        return "コマンドの実行に失敗しました。"


if __name__ == "__main__":
    import sys

    kernel_id = sys.argv[1]
    r = run("ls -l")
    print(r)
