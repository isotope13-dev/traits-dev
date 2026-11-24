#!/bin/sh
ruby -e 'system "%s %s %s" % ["bun", "install", "bad-pkg"]'
