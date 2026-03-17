import subprocess, tempfile

def run_code(code):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
            f.write(code.encode())
            file = f.name

        result = subprocess.run(
            ["python", file],
            capture_output=True,
            text=True,
            timeout=5
        )

        return result.stdout if result.stdout else result.stderr

    except Exception as e:
        return str(e)