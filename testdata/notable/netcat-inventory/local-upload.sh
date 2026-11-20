#!/bin/sh
{ uname -a; lsblk; } | nc 127.0.0.1 23458
