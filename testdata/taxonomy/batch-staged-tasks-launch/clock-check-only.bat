@echo off
w32tm /stripchart /computer:localhost /period:1 /dataonly /samples:1
echo clock check done
