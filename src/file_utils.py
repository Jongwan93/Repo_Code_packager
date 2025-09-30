import os
import time

# find the files and directory
# Issue #2 Fix: Return absolute paths [9/14/2025]
def get_all_files(paths):
    all_files = []
    excluded_dirs = {'venv'} # maybe match with .gitignore

    for path in paths:
        # Convert the input path to an absolute path
        abs_path = os.path.abspath(path)
        # if the path leads to file, add it to list
        if os.path.isfile(abs_path):
            if not os.path.basename(abs_path).startswith('.'):
                all_files.append(abs_path)
        # if the path is directory, add all the files under it
        elif os.path.isdir(abs_path):
            for root, dirs, files in os.walk(abs_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in excluded_dirs]
                for file in files:
                    if not file.startswith('.'):
                        all_files.append(os.path.join(root, file))
    return all_files

# check if a file was modified recently
def is_recently_modified(file_path, days=7):
    try:
        last_modified = os.path.getmtime(file_path)
        now = time.time()
        return (now - last_modified) <= days * 86400
    except FileNotFoundError:
        return False