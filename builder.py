import subprocess

def compile_and_log(source: str, test_file: str, log_path: str) -> bool:
    compile_cmd = f"gcc -fprofile-arcs -ftest-coverage {source} {test_file} -o test_exec"
    result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
    with open(log_path, 'w') as f:
        f.write(result.stdout + "\n" + result.stderr)
    return result.returncode == 0
