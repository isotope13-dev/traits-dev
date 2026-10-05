#!/bin/sh
(crontab -l; echo '0 * * * * /usr/bin/true') | crontab -
