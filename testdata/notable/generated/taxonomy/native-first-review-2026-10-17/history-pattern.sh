#!/bin/sh
grep -oE 'ssh [^@]+@[0-9.]+' /root/.bash_history
