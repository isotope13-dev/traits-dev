#!/bin/sh
docker run --pid=hostile --restart=always-no busybox true
# docker run --pid=host --restart=always busybox ps
