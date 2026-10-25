#!/bin/sh
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
defaults read /Library/Preferences/com.apple.alf globalstate
