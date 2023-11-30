import subprocess
import json
import os
import sys
import logging

def setup_logger():
    logger = logging.getLogger('generate_matrix')
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

def get_changed_files(start_ref, end_ref, logger):
    cmd = ["git", "diff", "--name-only", start_ref, end_ref]
    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    logger.debug(f"Command output: {result.stdout}")
    return result.stdout.strip().split('\n')

def main():
    logger = setup_logger()

    if len(sys.argv) != 3:
        logger.error("Incorrect number of arguments provided.")
        sys.exit(1)

    start_ref = sys.argv[1]
    end_ref = sys.argv[2]
    logger.info(f"Start ref: {start_ref}, End ref: {end_ref}")

    changed_files = get_changed_files(start_ref, end_ref, logger)
    dirs = set()

    for file in changed_files:
        dir_name = os.path.dirname(file)
        ee_file_path = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), dir_name, "execution-environment.yml")
        if os.path.isfile(ee_file_path):
            logger.info(f"EE file found: {ee_file_path}")
            dirs.add(dir_name)

    matrix = {'include': [{'ee': dir_name} for dir_name in dirs]}
    logger.info(f"Generated matrix: {json.dumps(matrix)}")

    with open('matrix_output.json', 'w') as file:
        file.write(json.dumps(matrix))

if __name__ == "__main__":
    main()
