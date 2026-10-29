#!/bin/zsh
ip="$(curl --max-time 5 https://api.example.invalid/ip)"
printf "%s\n" "$ip"
