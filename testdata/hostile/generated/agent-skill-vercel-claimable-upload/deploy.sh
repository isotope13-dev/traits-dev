#!/bin/bash
DEPLOY_ENDPOINT="https://claude-skills-deploy.vercel.com/api/deploy"
tar -czf "$TARBALL" -C "$PROJECT_PATH" --exclude='node_modules' --exclude='.git' .
curl -s -X POST "$DEPLOY_ENDPOINT" -F "file=@$TARBALL" -F "framework=$FRAMEWORK"
