# 🧪 Unit Test Generator for C/C++ using Local LLM (Ollama)

Automatically generate, refine, and test unit tests for C/C++ applications using a self-hosted LLM like Ollama (e.g., `llama3`, `codellama`). This tool compiles tests, checks build errors, and evaluates code coverage using `gcov`.

---

## 📁 Project Structure

unit-test-gen/
├── input/ # Input C/C++ files and generated test files
│ ├── sample.c # Sample C source file
│ ├── sample.h # Sample C header file
│ └── test_sample.c # LLM-generated unit test file
├── prompts/
│ └── test_prompt.yaml # Strict YAML prompt for LLM
├── main.py # Main script: generate, build, run, and coverage
├── ollama_client.py # Interface to self-hosted LLM (via Ollama CLI)
└── README.md

---

## 🚀 Features

- ✅ Generate unit tests using **Ollama** LLM
- 🛠️ Auto-retry test generation if build fails
- 📊 Measure line coverage using `gcov`
- ⚠️ Detect and eliminate **duplicate or invalid tests**
- 📦 YAML prompt-based control
- 📥 Uses `assert.h` (lightweight — no frameworks required)

---

## 🛠️ Setup Instructions

### 1. Install Dependencies

- GCC and `gcov` (for coverage)
- Python 3.8+
- [Ollama](https://ollama.com) (install + run locally)

### 2. Clone and Set Up

```bash
git clone https://github.com/yourusername/unit-test-gen.git
cd unit-test-gen

```

### 3. Install Python Libraries
```bash
pip install pyyaml

```

## 🧠 How It Works
YAML Prompt (prompts/test_prompt.yaml)

```
# instructions.yaml

task: "Generate C/C++ unit tests"

requirements:
  - Use assert-style tests (e.g., assert.h or Google Test if C++)
  - Include all necessary headers for the test to compile
  - Avoid test duplication
  - Ensure all functions are tested at least once
  - Avoid invalid inputs (e.g., division by 0, NULL pointer dereference)
  - Wrap all test cases inside a proper main() function
  - Use readable variable names and comments

formatting:
  - Use consistent indentation (4 spaces)
  - Avoid unnecessary whitespace
  - Comment each test with what it’s testing

output:
  - Provide only the test code, no explanation
  - Wrap all code in a single `main()` function if assert.h is used
  - Return valid compilable code only

language: "C"
```

## Running the Generator
```
python main.py
```

This does the following:
- Cleans up previous build & coverage files
- Sends sample.c + strict YAML prompt to Ollama
- Generates test_sample.c using LLM
- Builds and retries if build fails
- Runs the tests
- Uses gcov to print coverage metrics

## ⚙️ Running the LLM (Ollama)

```
bash

ollama run llama3
```

In ollama_client.py, the model name should match:

```
python
subprocess.run(["ollama", "run", "llama3", prompt_text])
```

llama3 can be changed to:
- codellama
- mistral
- phi
- any local model available in your Ollama setup

## 🧪 Sample Output
```
bash
✅ All tests passed.
📂 Files in 'input/' after running tests:
 - sample.c
 - sample.gcda
 - sample.gcno
 - sample.h
 - sample.o
 - test_sample.c
 - test_sample.gcda
 - test_sample.gcno
 - test_sample.o
 - test_binary.exe

📈 Line Coverage: 2/2 lines executed ✅ (100.0%)
```

