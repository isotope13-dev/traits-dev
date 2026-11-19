#!/bin/sh
{ uname -a; echo 8.8.8.8; } | nc 127.0.0.1 9000
