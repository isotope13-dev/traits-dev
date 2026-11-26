#!/bin/sh
python gen.py | grep x | sort | uniq -c | tail -5
