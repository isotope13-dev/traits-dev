#!/bin/sh
curl -fLsSo .licenserc.yaml https://config.example.invalid/license.yaml
curl --output ./.licenserc.yaml https://config.example.invalid/license.yaml
curl -fLsSo .licenserc.yaml https://config.example.invalid/.licenserc.yaml
