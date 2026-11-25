#!/bin/sh
# DigitalOcean Marketplace image build: install the base packages.
apt-get update -qq
apt-get install -y -qq ca-certificates curl
