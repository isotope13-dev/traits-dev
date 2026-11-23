#!/bin/sh
for artifact in ./build/*.zip; do
  sha256sum "$artifact"
done
