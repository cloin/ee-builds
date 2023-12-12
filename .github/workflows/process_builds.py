import json
import subprocess
import os

def run_command(command):
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command, check=True)

def main():
    with open('ee_matrix_output.json', 'r') as file:
        matrix = json.load(file)

    for item in matrix['include']:
        version = item['version']
        base_image = item.get('base_image', '')
        ee = item['ee']
        tag_suffix = "pr-95-840dbad"

        image_name = f"{ee}-{version}" if version != "default" else ee
        full_tag = f"{image_name}:{tag_suffix}"

        # Build command
        build_args = ['ansible-builder', 'build', '-v', '3', '--context=../' + ee,
                      '--tag=' + full_tag]

        if version != "default":
            build_args += ['--build-arg', f'EE_BASE_IMAGE={base_image}']

        run_command(build_args)

        # Create artifact file
        commands_file = f"commands-{image_name}.txt"
        with open(commands_file, 'w') as file:
            file.write(f"podman pull ghcr.io/cloin/{full_tag}\n")
            # Add more info as needed

if __name__ == "__main__":
    main()
