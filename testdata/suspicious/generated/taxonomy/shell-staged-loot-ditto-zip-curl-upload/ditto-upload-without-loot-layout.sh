#!/bin/bash
ditto -c -k "$HOME/Documents/notes" /tmp/out.zip
curl -sS -X POST --data-binary @/tmp/out.zip https://backup.example.com/api/upload
