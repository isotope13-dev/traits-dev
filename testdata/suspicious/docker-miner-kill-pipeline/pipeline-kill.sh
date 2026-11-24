#!/bin/sh
docker ps | grep mine | awk '{print $1}' | xargs docker kill
