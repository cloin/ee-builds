import subprocess
import json
import os
import sys

def get_changed_files_for_push(ancestor_commit, head_commit):
    cmd = ["git", "diff", "--name-only", ancestor_commit, head_commit]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def main():
    github_workspace = os.getenv('GITHUB_WORKSPACE')
    if len(sys.argv) == 3:
        ancestor_commit = sys.argv[1]
        head_commit = sys.argv[2]
        changed_files = get_changed_files_for_push(ancestor_commit, head_commit)
    else:
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
        ee_file_path = os.path.join(github_workspace, dir_name, "execution-environment.yml")
        if os.path.isfile(ee_file_path):
            dirs.add(dir_name)

    matrix = {'include': [{'ee': dir_name} for dir_name in dirs]}
    print(json.dumps(matrix))

if __name__ == "__main__":
    main()
