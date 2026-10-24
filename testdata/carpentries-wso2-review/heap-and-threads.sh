#!/bin/sh
jmap -dump:format=b,file="$out/heap.bin" "$pid"
jstack -l "$pid" > "$out/threads.txt"
