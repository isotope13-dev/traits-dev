#!/bin/bash
# echo -e '\x68\x69'
# base32 -d
printf '%s\n' "echo -e '\x68\x69'"
echo '\x68\x69'
echo -e 'hello'
echo -e '\143\165\162\154'
base32 input.bin
printf '%s\n' 'base32 --decode'
