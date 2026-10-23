#!/bin/sh
printf '%s\n' 'sysctl -n hw.memsize' 'date +%s'
sysctl -n hw.model
date +%Y
