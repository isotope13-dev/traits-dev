#!/bin/sh
realm=$(host -t txt _kerberos.$domain | head -1)
printf "%s\n" "$realm"
