#!/bin/sh
DEPLOY_ENDPOINT="https://claude-skills-deploy.vercel.com/api/deploy"
RESPONSE=$(curl -s -X POST "$DEPLOY_ENDPOINT" -F "file=@$TARBALL" -F "framework=$FRAMEWORK")
