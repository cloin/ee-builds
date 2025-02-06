import subprocess
import json
import os
import sys
import logging
import argparse
import yaml

def setup_logger(level):
    """Set up the logger with specified logging level."""
    logger = logging.getLogger('generate_matrix')
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

def get_changed_files(start_ref, end_ref, logger):
    """Get a list of changed files between two Git references."""
    cmd = ["git", "diff", "--name-only", start_ref, end_ref]
    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        logger.error(f"Git command failed with exit code {result.returncode}: {result.stderr}")
        sys.exit(1)

    logger.debug(f"Command output: {result.stdout}")
    return result.stdout.strip().split('\n')

def read_build_versions(ee_dir, logger):
    """Read build_versions.yml and return the build versions matrix."""
    versions_file = os.path.join(ee_dir, "build_versions.yml")
    if os.path.exists(versions_file):
        logger.info(f"Found build_versions.yml at: {versions_file}")
        with open(versions_file, 'r') as file:
            versions_data = yaml.safe_load(file)
            return versions_data.get('versions', [])
    return []

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate a matrix for GitHub Actions based on changed files.")
    parser.add_argument("-s", "--start-ref", required=True, help="The start Git reference.")
    parser.add_argument("-e", "--end-ref", required=True, help="The end Git reference.")
    parser.add_argument("-o", "--output-path", required=True, help="The output file path for the matrix JSON.")
    parser.add_argument("-l", "--log-level", default="INFO", choices=["DEBUG", "INFO"], help="Set the logging level (default: INFO).")
    return parser.parse_args()

def main():
    args = parse_arguments()
    log_level = logging.DEBUG if args.log_level == 'DEBUG' else logging.INFO
    logger = setup_logger(log_level)

    logger.info(f"Start ref: {args.start_ref}, End ref: {args.end_ref}")

    dirs = {}

    changed_files = get_changed_files(args.start_ref, args.end_ref, logger)
    
    for file in changed_files:
        dir_name = os.path.dirname(file)
        ee_file_path = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), dir_name, "execution-environment.yml")
        if dir_name not in dirs and os.path.isfile(ee_file_path):
            logger.info(f"EE file found: {ee_file_path}")
            versions = read_build_versions(os.path.join(os.getenv('GITHUB_WORKSPACE', ''), dir_name), logger)
            if versions:
                dirs[dir_name] = versions
            else:
                dirs[dir_name] = [{"version": "", "name": dir_name, "base_image": ""}]

    matrix = {"include": []}
    for dir_name, versions in dirs.items():
        for version in versions:
            matrix_entry = {
                "ee": dir_name,
                "version": version["version"],
                "name": f"{dir_name}-{version['version']}" if version["version"] else dir_name,
                "base_image": version["base_image"]
            }
            matrix["include"].append(matrix_entry)

    logger.info(f"Generated matrix: {json.dumps(matrix, indent=4)}")

    with open(args.output_path, 'w') as file:
        file.write(json.dumps(matrix))

if __name__ == "__main__":
    main()
