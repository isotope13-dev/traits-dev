#!/bin/bash
# Never run: chmod -R 777 "/Applications/Example.app"
# Never run: /Applications/Example.app/Contents/MacOS/Example --b "$PACKAGE_PATH"
ditto -x -k /tmp/docs-bundle.zip /tmp/docs-unpacked
echo "/Applications/Example.app/Contents/MacOS/Example"
