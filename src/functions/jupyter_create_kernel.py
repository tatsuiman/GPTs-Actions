import json
from jupyter_client import create_kernel


def run(language):
    kernel_id = create_kernel(language)
    return json.dumps({"kernel_id": kernel_id})


if __name__ == "__main__":
    import sys

    print(run(sys.argv[1]))
