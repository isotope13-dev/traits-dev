#!/bin/bash
# Support helper: migrates a preference plist to XML and flips one key.
# No installer hook, no fingerprint collection, no network upload.
CFG="$HOME/Library/Preferences/com.example.Helper.plist"
plutil -convert xml1 -o "${CFG}.xml" "${CFG}"
/usr/libexec/PlistBuddy -c "Set :RefreshEnabled bool true" "${CFG}"
CUR=$(/usr/libexec/PlistBuddy -c "Print :RefreshEnabled" "${CFG}")
echo "refresh: ${CUR}"
