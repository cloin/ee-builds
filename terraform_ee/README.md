# aws_ee
definition file for aws_ee

## Requirements:

Make sure to install ansible-builder

```
pip3 install ansible-builder
```

## Instructions

To build->

`ansible-builder build`

## Example publishing

```
$ podman login quay.io
Username: seanc@redhat.com
Password:
Login Succeeded!
$
```
You can see your newly created image in podman (Default):
```
$ podman images
REPOSITORY                                                                         TAG         IMAGE ID      CREATED         SIZE
localhost/ansible-execution-env                                                    latest      51278099b725  11 minutes ago  996 MB
<none>                                                                             <none>      b1b66b45526c  13 minutes ago  945 MB
<none>                                                                             <none>      e32d30b2f115  16 minutes ago  938 MB
quay.io/ansible/ansible-builder                                                    latest      8e8cbed25d34  22 hours ago    538 MB
registry.redhat.io/ansible-automation-platform-20-early-access/ee-supported-rhel8  2.0.0       85ca2003a842  2 months ago    920 MB
````

Make sure you have the destination made on your registry... and that you have write access or you will get an error.  For example on quay I needed to make this public because my hosting plan did not let me have a private registry, so it failed.

Now push->
podman push local-name public-published-name

Example:
```
$ podman push localhost/ansible-execution-env quay.io/acme_corp/aws_ee
Getting image source signatures
Copying blob e7ed17121dee done
Copying blob 8fbf8a5d89bc done
Copying blob 785573c4b945 done
Copying blob 0529b109eba6 done
Copying blob 4a155c756b32 done
Copying blob a114a5d855cd done
Copying blob 7a224c270209 done
Copying blob 48600caeab71 done
Copying config 51278099b7 done
Writing manifest to image destination
Copying config 51278099b7 [======================================] 3.2KiB / 3.2KiB
Writing manifest to image destination
Storing signatures
```

Boom, now you can sync your registry with Automation controller or another machine and use ansible-navigator!
