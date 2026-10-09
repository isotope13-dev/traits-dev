#!/bin/sh
ssh -vvv -p 10022 -i "$HOME/.ssh/host.id_rsa" root@localhost "uname -a;whoami;pwd"
