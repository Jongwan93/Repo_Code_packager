REPO_CODE_PACKAGER (Repository Context Packager)
RepoScriber is a command-line tool (CLI) that analyzes a local Git repository and generates a single, clean text file optimized for sharing with Large Language Models (LLMs). No more manually copy-pasting files when asking ChatGPT for help with your code!

The Problem
When developers ask LLMs for help with their code, the biggest challenge is providing enough context. Sharing snippets of code without the project's file structure, dependencies, and file relationships often leads to generic or unhelpful answers.

RepoScriber solves this by packaging all the essential information about your repository into one well-structured file, helping the LLM understand your project's architecture much more effectively.

Key Features
- Simple CLI Interface: Analyze your entire project, specific directories, or individual files with a single command.

- Project Structure Visualization: Automatically generates a tree view of your project's directory and file structure.

- Git Integration: Includes key Git metadata like the current branch and latest commit information.

- File Content Aggregation: Combines the content of all specified text files, separated by clear headers.

- Automatic .gitignore Handling: Smartly excludes files and directories listed in your .gitignore to keep the output clean and relevant.

- Save to File: Print the context directly to the console or use the -o option to save it to a .txt or .md file.

🛠️ Installation
Clone the repository:

Bash

git clone https://github.com/jongwan93/REPO_CODE_PACKAGER
cd REPO_CODE_PACKAGER
Set up and activate a virtual environment:

Bash

# Create a virtual environment
python -m venv venv
# Activate on macOS/Linux
source venv/bin/activate
# Activate on Windows
.\venv\Scripts\activate
Install dependencies:
If you used external libraries like pathspec, it's best practice to list them in a requirements.txt file.



License
This project is licensed under the MIT License.

