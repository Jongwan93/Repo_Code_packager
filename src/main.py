import argparse
import sys
import os
import time
from file_utils import get_all_files, is_recently_modified
from git_utils import get_git_info
from content_packager import create_structure_tree, format_file_contents, generate_summary
from toml_utils import load_config

TOOL_VERSION = "0.1.0"

def main():
    # ArgumentParser object creation
    parser = argparse.ArgumentParser(
        description="Repository Context Packager"
    )

    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = f"%(prog)s {TOOL_VERSION}"
    )

    # file or directory argument
    parser.add_argument(
        "paths",
        nargs = "+", # 1 or more
        help = "Paths to files or directories to include in the context."
    )

    # optional feature 1: Output to file
    parser.add_argument(
        "-o", "--output",
        help = "Path to the output file. If not specified, prints to standard output."
    )

    # optional feature 2: Token counting
    parser.add_argument(
        "--tokens",
        action = "store_true", #This makes it a flag, like --version
        help = "Estimate and display the token count for the context."
    )
    
    # includes files modified within 7 days
    parser.add_argument(
        "-r", "--recent",
        action="store_true",
        help="Only include files modified within the last 7 days"
    )
    
    # Lab3-1: adds line numbers to the output file
    parser.add_argument(
        "-l", "--line-numbers",
        action="store_true",
        help="Include line numbers in the file content output."
    )

    # Lab3-2: create directory tree structure
    parser.add_argument(
        "-d", "--dirs-only",
        action="store_true",
        help="Show only the directory structure without file contents."
    )

    #load default values from .toml config
    try:
        defaults = load_config(".repo-code-packager-config.toml")
    except RuntimeError as e:
        sys.exit(f"Runtime Error: {e}")
    if defaults:
        parser.set_defaults(**defaults)

    # pare the argument
    args = parser.parse_args()

    first_path_abs = os.path.abspath(args.paths[0])
    base_path = os.path.dirname(first_path_abs) if os.path.isfile(first_path_abs) else first_path_abs

    # get all the files from provided path
    file_list = get_all_files(args.paths)

    if args.recent:
        file_list = [f for f in file_list if is_recently_modified(f)]

    if not file_list:
        print("Error: No files found in the specified paths.", file=sys.stderr)
        sys.exit(1)

    git_info_str = get_git_info(base_path)
    structure_tree_str = create_structure_tree(file_list, base_path)
    file_contents_str, total_lines, total_chars = format_file_contents(file_list, base_path, args)
    summary_str = generate_summary(file_list, total_lines)
    
    recent_summary = ""
    if args.recent:
        recent_summary = "\n## Recent Changes\n"
        if file_list:
            for f in file_list:
                days_ago = int((time.time() - os.path.getmtime(f)) // 86400)
                recent_summary += f"- {os.path.basename(f)} (modified {days_ago} days ago)\n"
    else:
        recent_summary += "No files modified in the last 7 days.\n"

    output_parts = [
        f"""# Repository Context

## File System Location

{base_path}

## Git Info

{git_info_str}

## Structure

{structure_tree_str}"""
    ]
    
    if not args.dirs_only:
        output_parts.append(f"## File Contents\n\n{file_contents_str}")
    
    if args.recent:
        output_parts.append(recent_summary)

    output_parts.append(f"""## Summary

{summary_str}""")
    
    final_output = "\n\n".join(output_parts)

    # optional feature 2: Token counting
    if args.tokens:
        estimated_tokens = total_chars // 4
        print(f"Estimated tokens: {estimated_tokens}", file=sys.stderr)

    # optional feature 1: Output to file
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(final_output.strip())
            print(f"Context successfully written to {args.output}", file=sys.stderr)
        except IOError as e:
            print(f"Error writing to file {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(final_output.strip())

if __name__ == "__main__":
    main()