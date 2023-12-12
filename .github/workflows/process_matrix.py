import json
import os
import sys
import logging
import yaml

def setup_logger():
    logger = logging.getLogger('process_matrix')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def process_matrix(input_path):
    logger = setup_logger()
    ee_name = os.path.basename(os.getcwd()) 
    logger.info(f"Generating EE build matrix for: {ee_name}")

    matrix_file = os.path.join(input_path, 'matrix.yml')
    matrix = {'include': []}

    if os.path.exists(matrix_file):
        logger.info(f"Found matrix.yml at: {matrix_file}")
        with open(matrix_file, 'r') as file:
            versions = yaml.safe_load(file).get('versions', [])
            for version in versions:
                matrix['include'].append({
                    'ee': ee_name,
                    'version': version.get('name', 'default'),
                    'base_image': version.get('base_image', '')
                })
    else:
        logger.info("No matrix.yml found. Using default build configuration.")
        matrix['include'].append({'ee': ee_name, 'version': 'default', 'base_image': ''})

    logger.info(f"Generated matrix: {json.dumps(matrix, indent=4)}")
    return matrix

def main():
    if len(sys.argv) != 2:
        print("Usage: process_matrix.py <input-path>")
        sys.exit(1)

    input_path = sys.argv[1]
    matrix = process_matrix(input_path)
    print(json.dumps(matrix))
    with open('ee_matrix_output.json', 'w') as outfile:
        json.dump(matrix, outfile)

if __name__ == "__main__":
    main()
