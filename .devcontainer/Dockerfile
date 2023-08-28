# Use Fedora 38 as the base image
FROM fedora:38

# Install Java OpenJDK, python3-pip, and ansible
RUN dnf --assumeyes install git python3-pip && \
    pip3 install ansible ansible-builder
