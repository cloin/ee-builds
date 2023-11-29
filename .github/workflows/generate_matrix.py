import subprocess
import json
import os

def get_changed_files_for_push():
    # get the hash of the immediate ancestor commit
    ancestor_commit = subprocess.run(
        ["git", "rev-parse", "HEAD^1"], capture_output=True, text=True
    ).stdout.strip()

    # get the list of changed files compared to the ancestor
    cmd = ["git", "diff", "--name-only", ancestor_commit, "HEAD"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def main():
    # determine context (PR or push)
    is_pr = os.getenv('GITHUB_BASE_REF') is not None and os.getenv('GITHUB_HEAD_REF') is not None

    if is_pr:
        base_ref = os.getenv('GITHUB_BASE_REF')
        head_ref = os.getenv('GITHUB_HEAD_REF')
        cmd = ["git", "diff", "--name-only", f"origin/{base_ref}", f"origin/{head_ref}"]
    else:
        cmd = ["git", "diff", "--name-only", "HEAD^1", "HEAD"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    changed_files = result.stdout.strip().split('\n')

    dirs = set()
    for file in changed_files:
        dir_name = os.path.dirname(file)
        if os.path.isfile(f"{dir_name}/execution-environment.yml"):
            dirs.add(dir_name)

    matrix = {'include': [{'ee': dir_name} for dir_name in dirs]}
    print(json.dumps(matrix))

if __name__ == "__main__":
    main()
