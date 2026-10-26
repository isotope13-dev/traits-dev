#!/bin/sh
tar cf archive.tar --checkpoint=1 --checkpoint-action=exec=sh .
