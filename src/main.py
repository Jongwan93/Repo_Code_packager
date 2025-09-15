# main.py
import argparse
import sys
import os
import subprocess

TOOL_VERSION = "0.1.0"

# find the files and directory
# Issue #2 Fix: Return absolute paths [9/14/2025]
def get_all_files(paths):
    all_files = []
    for path in paths:
        # Convert the input path to an absolute path
        abs_path = os.path.abspath(path)
        # if the path leads to file, add it to list
        if os.path.isfile(abs_path):
            all_files.append(abs_path)
        # if the path is directory, add all the files under it
        elif os.path.isdir(abs_path):
            for root, _, files in os.walk(abs_path):
                for file in files:
                    all_files.append(os.path.join(root, file))
    return all_files

# TODO: use subprocess module to execute git commands and get newest commit and branch name
def get_git_info():
    pass

# TODO: Currently, file names are just listed on the terminal. Must create tree structure reflecting depth of file and directories
def create_structure_tree(file_list):
    pass

# TODO: gather the file contents and merge into a big string block.
# consider try catch.
def format_file_contents(file_list):
    pass

# TODO: calculate entire number of files and number of lines.
def generate_summary(file_list, total_lines):
    pass

def main():
    # ArgumentParser object creation
    parser = argparse.ArgumentParser(
        description="Repository Context Packager"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {TOOL_VERSION}"
    )

    # file or directory argument
    parser.add_argument(
        "paths",
        nargs="+", # 1 or more
        help="Paths to files or directories to include in the context."
    )

    # pare the argument
    args = parser.parse_args()

    # test print
    print("Directory Path:", args.paths)

    # get all the files from provided path
    file_list = get_all_files(args.paths)

    # test print
    print("file found:")
    for f in file_list:
        print(f"- {f}")

    # TODO: call the helper functions
    # Store the return value from each function
    # put all the return value into a single output.txt file

if __name__ == "__main__":
    main()