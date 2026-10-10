#!/bin/sh
appliance="$1"
admin_session="$2"
websocat "wss://$appliance/wsproxy?bmID=1234&serviceType=SSH&host=::1&port=8188"
