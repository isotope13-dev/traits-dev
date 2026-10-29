#!/bin/sh
service="svc:/application/demo:default"
svccfg -s "$service" setprop config/interval = integer: 30
svcadm refresh "$service"
svcadm enable "$service"
