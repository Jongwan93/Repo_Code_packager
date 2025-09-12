# main.py
import argparse
import sys
import os

TOOL_VERSION = "0.1.0"

# find the files and directory
def get_all_files(paths):
    all_files = []
    for path in paths:
        # if the path leads to file, add it to list
        if os.path.isfile(path):
            all_files.append(path)
        # if the path is directory, add all the files under it
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    # os.path.join completes the file path
                    all_files.append(os.path.join(root, file))
    return all_files

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

if __name__ == "__main__":
    main()