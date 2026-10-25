#!/bin/sh
ioreg -n Root -d1 | awk '/CGSSessionScreenIsLocked/ {print $NF}'
