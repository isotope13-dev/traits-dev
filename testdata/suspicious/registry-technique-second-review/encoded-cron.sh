#!/bin/sh
(crontab -l; echo '* * * * * echo ZWNobyBoZWxsbwo= | base64 --decode | sh') | crontab -
