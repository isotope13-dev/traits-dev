#!/bin/sh
sysctl -n hw.model
sysctl -n machdep.cpu.brand_string
sw_vers -productVersion
