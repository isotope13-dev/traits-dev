#!/bin/bash
# Static fixture: select decoding, independently of the input.
base32 -d data.txt
/usr/bin/base32 --decode data.txt
