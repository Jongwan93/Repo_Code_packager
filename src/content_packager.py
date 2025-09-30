import os
import sys
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound

# create tree structure reflecting depth of file and directories
def create_structure_tree(file_list, base_path):
    tree = {}
    for file_path in file_list:
        relative_path = os.path.relpath(file_path, base_path)
        parts = relative_path.split(os.sep)

        current_level = tree
        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        current_level[parts[-1]] = None

    def generate_tree_string(d, indent=''):
        lines = []
        # Sort items to make the output consistent every time.
        items = sorted(d.items())
        for i, (name, content) in enumerate(items):
            is_last = i == len(items) - 1
            prefix = '└── ' if is_last else '├── '
            lines.append(f"{indent}{prefix}{name}")
            if isinstance(content, dict): # If it's a directory, go one level deeper.
                connector = '    ' if is_last else '│   '
                lines.extend(generate_tree_string(content, indent + connector))
        return lines
    return "\n".join(generate_tree_string(tree))

# gather the file contents and merge into a big string block.
def format_file_contents(file_list, base_path, args):
    all_contents = []
    total_lines = 0
    total_chars = 0
    MAX_FILE_SIZE_KB = 16
    MAX_BYTES = MAX_FILE_SIZE_KB * 1024

    for file_path in sorted(file_list):
        try:
            file_size = os.path.getsize(file_path)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                relative_path = os.path.relpath(file_path, base_path)
                all_contents.append(f"### File: {relative_path}")
                
                content = f.read()

                # Lab3-1: add line numbers to the output file
                if args.line_numbers:
                    lines = content.splitlines()
                    numbered_lines = [f"{i+1}: {line}" for i, line in enumerate(lines)]
                    content = "\n".join(numbered_lines)

                if file_size > MAX_BYTES:
                    content = content[:MAX_BYTES]
                    truncation_note = f"\n... (file truncated due to size > {MAX_FILE_SIZE_KB}KB)"
                    content += truncation_note

                lang_name = ""
                try:
                    # find the language from file name
                    lexer = guess_lexer_for_filename(file_path, content)
                    lang_name = lexer.aliases[0] if lexer.aliases else ""
                except ClassNotFound:
                    # if it failes to find language name
                    pass

                # Add the content inside a markdown code block.
                all_contents.append(f"```{lang_name}\n{content}\n```")
                
                # Count lines for the summary later.
                total_lines += content.count('\n') + 1
                total_chars += len(content)

        except Exception as e:
            print(f"Error reading file {file_path}: {e}", file=sys.stderr)
    return "\n\n".join(all_contents), total_lines, total_chars

# calculate entire number of files and number of lines.
def generate_summary(file_list, total_lines):
    file_count = len(file_list)
    summary_string = (
        f"- Total files: {file_count}\n"
        f"- Total lines: {total_lines}"
    )
    return summary_string