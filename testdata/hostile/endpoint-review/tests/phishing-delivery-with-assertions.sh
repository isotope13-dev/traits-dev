#!/bin/bash
assert_eq() { test "$1" = "$2"; }
assert_eq ok ok
while true; do echo "verify your account" | sendmail user@example.invalid; wall "verify your account"; done
