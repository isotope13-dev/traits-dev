#!/bin/bash
RUNAPIS="${ACTIONS_RUNTIME_URL}_apis/pipelines/workflows/${GITHUB_RUN_ID}/artifacts"
FCRU=$(curl -sS -X POST "$RUNAPIS?api-version=6.0-preview" -d '{"Type":"actions_storage","Name":"build"}' | python3 -c 'import json,sys;print(json.load(sys.stdin)["fileContainerResourceUrl"])')
curl -sS -X PUT "$FCRU&itemPath=build.tgz" --data-binary @build.tgz
