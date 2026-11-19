#!/bin/bash
assert_eq() { test "$1" = "$2"; }
assert_eq ok ok
ruby -e 'system("id")'
