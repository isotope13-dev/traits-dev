#!/bin/sh
sed -i 's#TZ=.*#TZ=UTC#'; id; #' /etc/sysconfig/clock
