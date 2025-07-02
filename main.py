import os
import subprocess
import glob
import yaml
from typing import Tuple
from ollama_client import generate_tests_ollama

INPUT_FILE = "input/sample.c"
TEST_FILE = "input/test_sample.c"
BINARY_PATH = "input/test_binary"
SOURCE_DIR = "input"
PROMPT_YAML = "prompts/test_prompt.yaml"

BUILD_CMD = f"gcc -Wall -fprofile-arcs -ftest-coverage -o {BINARY_PATH} input/sample.c input/test_sample.c"

def clean_coverage_files():
    print("🧹 Cleaning old coverage files...")
    for pattern in ["input/*.gcda", "input/*.gcno", "input/*.gcov"]:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                print(f"🗑️  Deleted: {file}")
            except Exception as e:
                print(f"⚠️  Could not delete {file}: {e}")

def compile_tests() -> Tuple[bool, str]:
    try:
        result = subprocess.run(
            BUILD_CMD,
            shell=True,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stderr + result.stdout
    except Exception as e:
        return False, str(e)

def save_test_code(test_code: str):
    os.makedirs(SOURCE_DIR, exist_ok=True)
    with open(TEST_FILE, "w") as f:
        f.write(test_code.strip())

def run_tests() -> Tuple[bool, str, str]:
    binary_path = os.path.abspath(BINARY_PATH)
    try:
        result = subprocess.run(
            [binary_path],
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def build_prompt_from_yaml(yaml_path: str) -> str:
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    parts = []
    if "language" in data:
        parts.append(f"Language: {data['language']}")
    if "objective" in data:
        parts.append(f"Objective: {data['objective']}")
    if "requirements" in data:
        parts.append("Requirements:")
        parts.extend([f"- {req}" for req in data["requirements"]])

    return "\n".join(parts)

def run_coverage():
    print("📊 Running gcov for coverage...")

    # Run gcov (will generate sample.c.gcov in current working directory)
    result = subprocess.run("gcov input/sample.c -o input", shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

    gcov_file = os.path.join(os.getcwd(), "sample.c.gcov")  # use absolute path

    if not os.path.exists(gcov_file):
        print("❌ No .gcov file generated.")
        return

    executed = 0
    total = 0

    with open(gcov_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) < 3:
                continue
            exec_marker = parts[0].strip()
            if exec_marker == "#####":
                total += 1
            elif exec_marker.isdigit():
                executed += 1
                total += 1

    if total > 0:
        percent = executed * 100 / total
        print(f"\n📈 Line Coverage: {executed}/{total} lines executed ✅ ({percent:.1f}%)")
    else:
        print("⚠️ No executable lines found.")


def main():
    clean_coverage_files()

    with open(INPUT_FILE, "r") as f:
        code = f.read()

    prompt = build_prompt_from_yaml(PROMPT_YAML)
    print("🧠 Generating unit tests...")
    test_code = generate_tests_ollama(code, prompt)

    if "Timeout" in test_code or not test_code.strip():
        print("❌ Timeout: Model took too long to respond.")
        print("⚠️  Skipping test generation to avoid overwriting existing test_sample.c.")
        return

    save_test_code(test_code)

    print("⚙️  Compiling tests...")
    success, logs = compile_tests()

    if not success:
        print("❌ Build failed. Retrying with LLM using logs...")
        logs = logs[-1000:]
        retry_prompt = f"""The following C unit test code failed to compile. Please correct it.

### Original Code
{code}

### Broken Test Code
{test_code}

### Compiler Logs
{logs}

Return corrected C unit tests using assert.h wrapped in int main(). No explanation.
"""
        fixed_test_code = generate_tests_ollama(code, retry_prompt)
        save_test_code(fixed_test_code)

        print("🔁 Re-compiling fixed test...")
        success, logs = compile_tests()
        if not success:
            print("❌ Final build failed.")
            print(logs)
            return

    print("✅ Build succeeded.")
    print("🚀 Running tests...")
    passed, stdout, stderr = run_tests()

    print("STDOUT:\n", stdout)
    print("STDERR:\n", stderr)

    if passed:
        print("✅ All tests passed.")
    else:
        print("❌ Some tests failed (non-zero exit code).")

    print("\n📂 Files in 'input/' after running tests:")
    for f in os.listdir(SOURCE_DIR):
        print(" -", f)

    print("🧮 Now running line coverage check using gcov...")
    run_coverage()

if __name__ == "__main__":
    print("\n🔍 Files in 'input/' after compilation:")
    for f in os.listdir("input"):
        print(" -", f)
