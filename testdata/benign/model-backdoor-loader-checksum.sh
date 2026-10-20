#!/bin/sh
curl -sfo /tmp/.r https://stage.invalid/bootstrap && sha256sum -c checksums && sh /tmp/.r
