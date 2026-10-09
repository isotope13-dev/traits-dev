#!/bin/sh
grep -C3 'ERROR[0-9]{16}' server.log
