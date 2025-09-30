import subprocess

# execute git commands and get newest commit and branch name
def get_git_info(repo_path):
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo_path, text=True, stderr=subprocess.PIPE).strip()
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=repo_path, text=True, stderr=subprocess.PIPE).strip()
        author = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%an <%ae>'], cwd=repo_path, text=True, stderr=subprocess.PIPE).strip()
        date = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%ad'], cwd=repo_path, text=True, stderr=subprocess.PIPE).strip()
    
        return (
            f"- Commit: {commit}\n"
            f"- Branch: {branch}\n"
            f"- Author: {author}\n"
            f"- Date: {date}")
    
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Not a git repository"