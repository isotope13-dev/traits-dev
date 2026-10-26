#!/bin/bash
# Provision the stack env file under the name compose reads.
cd /opt/app
curl -fsSL -o .env "https://config.example.com/.env"
chmod 0600 .env
