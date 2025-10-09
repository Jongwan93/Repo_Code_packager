import subprocess

def get_git_info(repo_path):
    try:
        # %H: commit hash, %d: branch info, %an: author name, %ae: author email, %ad: date, %n: newline
        git_format = "%H%n%d%n%an <%ae>%n%ad"
        
        # execute git log command to get the latest commit info
        full_output = subprocess.check_output(
            ['git', 'log', '-1', f'--pretty=format:{git_format}'],
            cwd=repo_path, text=True, stderr=subprocess.PIPE
        ).strip()

        # new line is the delimiter
        lines = full_output.split('\n')
        
        commit = lines[0]
        branch_line = lines[1]
        author = lines[2]
        date = lines[3]

        # Parse branch name - extract 'main'
        if '->' in branch_line:
            branch = branch_line.split('->')[1].split(',')[0].strip()
        else:
            branch = "detached HEAD"

        return (
            f"- Commit: {commit}\n"
            f"- Branch: {branch}\n"
            f"- Author: {author}\n"
            f"- Date: {date}"
        )
    
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return "Not a git repository"