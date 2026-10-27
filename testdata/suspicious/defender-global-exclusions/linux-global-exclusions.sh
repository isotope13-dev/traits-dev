#!/bin/sh
mdatp exclusion folder add --path /var/log/ --scope global
mdatp exclusion process add --path /usr/bin/cat --scope global
