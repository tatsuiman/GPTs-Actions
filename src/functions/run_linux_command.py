import subprocess


def run(cmd):
    r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {
        "returncode": r.returncode,
        "stdout": r.stdout.decode(),
        "stderr": r.stderr.decode(),
    }
