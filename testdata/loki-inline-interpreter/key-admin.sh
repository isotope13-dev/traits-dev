#!/bin/sh
ssh -i deployment_key admin@server "python3 -c 'import platform; print(platform.system())'"
