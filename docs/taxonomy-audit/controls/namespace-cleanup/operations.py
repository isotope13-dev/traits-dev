# Inert source examples for the distinct namespace and root operations.
command = "unshare -Urn"
flag = "CLONE_NEWUSER CLONE_NEWNET setns"
root_command = "chroot /host /bin/sh"
root_argv = '["chroot", "/mnt"]'
