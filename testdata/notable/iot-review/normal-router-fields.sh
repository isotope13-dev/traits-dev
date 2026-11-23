#!/bin/sh
printf '%s\n' 'operation=write&country=US'
printf '%s\n' '<language>en-US</language>'
printf '%s\n' '<NewNTPServer1>pool.ntp.org</NewNTPServer1>'
printf '%s\n' 'remote_host=192.0.2.1'
printf '%s\n' '/etc/init.d/backup' '/etc/rc.local'
