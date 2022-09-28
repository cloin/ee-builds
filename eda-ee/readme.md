## Notes:
The `playbooks` dir is needed right now while working on event driven automation with ansible. Currently, the eda project imported does not pass playbooks back to the EE. This `playbooks` dir is a workaround. 

`execution-environment.yml` uses a docker command `ADD` to pull the contents of `playbooks` into the generated image. Usually, this would result in an error because the container context is created in a subdirectory called `context` but I've adjusted the `ansible-builder build` command using the `--context` flag to set it to the same as this directory so the build context has access to the playbooks directory. 
