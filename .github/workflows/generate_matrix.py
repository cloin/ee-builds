import subprocess
import json
import os
import sys
import logging

def setup_logger():
    logger = logging.getLogger('generate_matrix_logger')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def get_changed_files_for_push(ancestor_commit, head_commit, logger):
    cmd = ["git", "diff", "--name-only", ancestor_commit, head_commit]
    result = subprocess.run(cmd, capture_output=True, text=True)
    logger.debug(f"Changed files: {result.stdout}")
    return result.stdout.strip().split('\n')

def main():
    logger = setup_logger()
    github_workspace = os.getenv('GITHUB_WORKSPACE')
    logger.debug(f"GitHub workspace: {github_workspace}")

    if len(sys.argv) == 3:
        ancestor_commit = sys.argv[1]
        head_commit = sys.argv[2]
        changed_files = get_changed_files_for_push(ancestor_commit, head_commit, logger)
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
        logger.debug(f"Checking EE file at: {ee_file_path}")
        if os.path.isfile(ee_file_path):
            dirs.add(dir_name)
            logger.debug(f"EE file found, adding '{dir_name}' to matrix.")

    matrix = {'include': [{'ee': dir_name} for dir_name in dirs]}
    logger.info(f"Generated matrix: {json.dumps(matrix)}")
    print(json.dumps(matrix))

if __name__ == "__main__":
    main()
