#!/bin/sh
export GLIBC_TUNABLES=glibc.malloc.trim_threshold=1024
printf '%s\n' gconv_init
