#!/bin/sh
# Static fixture; a writability probe chained with && backgrounds nothing.
# Guards the lone-& requirement on hidden-stage-background-exec.
>/var/run/.x&&cd /var/run;>/tmp/.x&&cd /tmp;>/var/.x&&cd /var
