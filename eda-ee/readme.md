## Notes:
The `playbooks` dir is needed right now while working on event driven automation with ansible. Currently, the eda project imported does not pass playbooks back to the EE. This `playbooks` dir is a workaround. 

`execution-environment.yml` uses a docker command `ADD` to pull the contents of `playbooks` into the generated image. 
```
    ADD playbooks /runner/project
```
Usually, this would result in an error because the container context is created in a subdirectory called `context`...
```
[3/3] STEP 4/9: ADD ../playbooks /runner/project
Error: error building at STEP "ADD ../playbooks /runner/project": checking on sources under "/home/runner/work/ee-builds/ee-builds/eda-ee/eda-ee": possible escaping context directory error: copier: stat: "/playbooks": no such file or directory
```
...but I've adjusted the `ansible-builder build` command using the `--context` flag to set it to the same as this directory so the build context has access to the playbooks directory. 

The build task looks like this:
```
      - name: Build image
        id: build-image
        working-directory: ${{ inputs.EE_FOLDER_NAME }}
        run: |
          ansible-builder build \
          --context=../${{ inputs.EE_FOLDER_NAME }} \
          --tag=${{ inputs.EE_FOLDER_NAME }}:${{ inputs.EE_IMAGE_TAG }} \
          --tag=${{ inputs.EE_FOLDER_NAME }}:${{ github.sha }}
```

and generates a Containerfile that looks like this:
```
ARG EE_BASE_IMAGE=registry.redhat.io/ansible-automation-platform-22/ee-minimal-rhel8:latest
ARG EE_BUILDER_IMAGE=quay.io/ansible/ansible-builder:latest

FROM $EE_BASE_IMAGE as galaxy
ARG ANSIBLE_GALAXY_CLI_COLLECTION_OPTS=
USER root

ADD _build/ansible.cfg ~/.ansible.cfg

ADD _build /build
WORKDIR /build

RUN ansible-galaxy role install -r requirements.yml --roles-path "/usr/share/ansible/roles"
RUN ANSIBLE_GALAXY_DISABLE_GPG_VERIFY=1 ansible-galaxy collection install $ANSIBLE_GALAXY_CLI_COLLECTION_OPTS -r requirements.yml --collections-path "/usr/share/ansible/collections"

FROM $EE_BUILDER_IMAGE as builder

COPY --from=galaxy /usr/share/ansible /usr/share/ansible

ADD _build/requirements.txt requirements.txt
ADD _build/bindep.txt bindep.txt
RUN ansible-builder introspect --sanitize --user-pip=requirements.txt --user-bindep=bindep.txt --write-bindep=/tmp/src/bindep.txt --write-pip=/tmp/src/requirements.txt
RUN assemble

FROM $EE_BASE_IMAGE
USER root
RUN pip3 install --upgrade pip setuptools

COPY --from=galaxy /usr/share/ansible /usr/share/ansible

COPY --from=builder /output/ /output/
RUN /output/install-from-bindep && rm -rf /output/wheels
ADD playbooks /runner/project
WORKDIR /runner/project
LABEL quay.expires-after="45d"
```
