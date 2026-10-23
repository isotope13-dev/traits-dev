#!/bin/sh
ssh user@server uptime; perl -e 'select(undef,undef,undef,0.01)'
