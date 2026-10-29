#!/bin/sh
perl -e '@parts = split("=", <>); print $parts[1];'
