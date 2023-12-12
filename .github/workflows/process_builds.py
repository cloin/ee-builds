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
        tag_suffix = f"{version}-pr-95-840dbad" if version != "default" else "pr-95-840dbad"
        ee = item['ee']

        # Build command
        build_args = ['ansible-builder', 'build', '-v', '3', '--context=../' + ee,
                      '--tag=' + ee + ':' + tag_suffix]

        if version != "default":
            build_args += ['--build-arg', f'EE_BASE_IMAGE={base_image}']

        run_command(build_args)

        # Create artifact file
        commands_file = f"commands-{ee}-{version}.txt"
        with open(commands_file, 'w') as file:
            file.write(f"podman pull ghcr.io/cloin/{ee}:{tag_suffix}\n")
            # Add more info as needed

if __name__ == "__main__":
    main()
