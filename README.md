# REPO_CODE_PACKAGER (Repository Context Packager)

REPO_CODE_PACKAGER is a command-line tool (CLI) that analyzes a local Git repository and generates a single, clean text file optimized for sharing with Large Language Models (LLMs). No more manually copy-pasting files when asking ChatGPT for help with your code!

## The Problem

When developers ask LLMs for help with their code, the biggest challenge is providing enough context. Sharing snippets of code without the project's file structure, dependencies, and file relationships often leads to generic or unhelpful answers.

REPO_CODE_PACKAGER solves this by packaging all the essential information about your repository into one well-structured file, helping the LLM understand your project's architecture much more effectively.

## Prerequisites

This script requires **Python 3** to be installed on your system.

1.  **Install Python 3**

    - If you don't have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

2.  **Clone the Repository**
    - Open your terminal (or Git Bash on Windows) and run the following command to download the project:
      ```bash
      git clone <YOUR_REPOSITORY_URL>
      cd <YOUR_REPOSITORY_FOLDER_NAME>
      ```
3.  **Install Dependencies**

    - This project uses third-party libraries listed in `requirements.txt`. Install them using pip:

    - **On macOS / Linux:**
      ```bash
      pip3 install -r requirements.txt
      ```
    - **On Windows:**
      ```bash
      pip install -r requirements.txt
      ```
      or
      ```bash
      py -3 -m pip install -r requirements.txt
      ```

## Usage

To run the program, navigate to the project's root directory (the folder containing the `src` directory) and use the following commands in your terminal.

### 🍎 On macOS / Linux

It's common to use the `python3` command on macOS and Linux systems.

- **Basic Usage (analyze the current directory):**

  ```bash
  python3 -m src.main .
  ```

- **Save output to a file:**

  ```bash
  python3 -m src.main . -o output.txt
  ```

- **Include only recent files and add line numbers:**
  ```bash
  python3 -m src.main . --recent --line-numbers
  ```

### On Windows

On Windows, you can use the `python` or `py -3` command.

- **Basic Usage (analyze the current directory):**

  ```bash
  python -m src.main .
  ```

  or

  ```bash
  py -3 -m src.main .
  ```

- **Save output to a file:**

  ```bash
  python -m src.main . -o output.txt
  ```

- **Include only recent files and add line numbers:**
  ```bash
  python -m src.main . --recent --line-numbers
  ```

---

## Key Features

| positional arguments | description                                           |
| -------------------- | ----------------------------------------------------- |
| **paths**            | Path to the repository / files in the same repository |

| options                   | description                                              |
| ------------------------- | -------------------------------------------------------- |
| **-h, --help**            | show this help message and exit                          |
| **--version, -v**         | show program's version number and exit                   |
| **--output, -o [OUTPUT]** | Output filename                                          |
| **--tockens**             | Estimate and display the token count for the context     |
| **--recent, -r [RECENT]** | Only include files modified within the last 7 days       |
| **--line-number, -l**     | Include line number when displaying file content output  |
| **--dirs-only, -d**       | Show only directory structure tree without file contents |

## Set Flag in .toml Configuration file

User can set values of flag in **.repo-code-packager-config.toml** configuration file to change the default flag value.  
Note that **.repo-code-packager-config.toml** should be in the same directory as **main.py**, and command line args can override the default values.

# License

This project is licensed under the MIT License.
