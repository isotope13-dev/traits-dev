#!/bin/sh
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
rm -rf "$SCRIPTPATH/build"
rm -f "$SCRIPTPATH/sources.list"
