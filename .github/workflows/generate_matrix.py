import subprocess
import json
import os

def get_changed_files(base_ref, head_ref):
    cmd = f"git diff --name-only origin/{base_ref}...origin/{head_ref}".split()
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def main():
    base_ref = os.getenv('GITHUB_BASE_REF') or os.getenv('INPUT_BASE_REF')
    head_ref = os.getenv('GITHUB_HEAD_REF') or os.getenv('INPUT_HEAD_REF')
    changed_files = get_changed_files(base_ref, head_ref)
    dirs = set()

    for file in changed_files:
        dir_name = os.path.dirname(file)
        if os.path.isfile(f"{dir_name}/execution-environment.yml"):
            dirs.add(dir_name)

    matrix = {'include': [{'ee': dir_name} for dir_name in dirs]}
    print("Matrix:", matrix)  # Debugging output
    print(json.dumps(matrix))

if __name__ == "__main__":
    main()
