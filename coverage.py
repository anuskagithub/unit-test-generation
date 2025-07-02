import subprocess

def run_coverage():
    subprocess.run("./test_exec", shell=True)
    subprocess.run("gcov *.c", shell=True)

def get_coverage_summary() -> str:
    with open("*.c.gcov", "r") as f:
        return f.read()
