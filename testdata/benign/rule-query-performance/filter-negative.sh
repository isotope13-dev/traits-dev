#!/bin/sh
env HOME=value | grep token
printenv TOKEN | grep token
env | grep -v token
env | grep -i -i token
env | grep token /dev/stdin
env | grep tokenizer
env | grep token < input
