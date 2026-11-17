#!/bin/bash
DEPLOY_ENDPOINT="https://codex-deploy-skills.vercel.sh/api/deploy"
tar -czf "$TARBALL" -C "$PROJECT_PATH" .
curl -s -X POST "$DEPLOY_ENDPOINT" -F "file=@$TARBALL" -F "framework=$FRAMEWORK"
