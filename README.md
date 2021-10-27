# Build execution environments with `ansible-builder`
## Building execution environment images for use in [ansible workshops](https://github.com/ansible/workshops)
### This repo responds to modifications on `main` by building a new container image with Github Actions to be used as an execution environment for Ansible Automation Platform 2.


[![ServiceNow EE build](https://github.com/cloin/ee-builds/actions/workflows/servicenow-ee-build.yml/badge.svg)](https://github.com/cloin/ee-builds/actions/workflows/servicenow-ee-build.yml) [![Windows EE build](https://github.com/cloin/ee-builds/actions/workflows/windows-ee-build.yml/badge.svg)](https://github.com/cloin/ee-builds/actions/workflows/windows-ee-build.yml) [![f5 EE build](https://github.com/cloin/ee-builds/actions/workflows/f5-ee-build.yml/badge.svg)](https://github.com/cloin/ee-builds/actions/workflows/f5-ee-build.yml)

### Contributions
The directories in this repository should follow the format that `ansible-builder` expects. See [servicenow-ee](https://github.com/cloin/ee-builds/tree/main/servicenow-ee) as an example. The name you give the directory will be the name of the image. `ansible-builder` only accepts one tag at the moment, and the default is set to latest. You can also copy the [servicenow-ee workflow](https://github.com/cloin/ee-builds/blob/main/.github/workflows/servicenow-ee-build.yml) file and adjust the parameters on lines 2 and 25-27. Questions? Open an issue!


### Useful documentation and links
- [Ansible Automation Platform](https://www.ansible.com/products/automation-platform)
- [ansible-navigator](https://github.com/ansible/ansible-navigator)
- [ansible-builder](https://github.com/ansible/ansible-builder)
- [GitHub Actions quickstart](https://docs.github.com/en/actions/quickstart)
- [GitHub environments](https://docs.github.com/en/actions/deployment/using-environments-for-deployment)
- [redhat-actions/podman-login](https://github.com/redhat-actions/podman-login)
- [redhat-actions/push-to-registry](https://github.com/redhat-actions/push-to-registry)
