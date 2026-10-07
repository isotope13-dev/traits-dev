#!/bin/bash
for account in a b; do
  for candidate in c d; do
    echo "${account}:${candidate}"
  done
done
