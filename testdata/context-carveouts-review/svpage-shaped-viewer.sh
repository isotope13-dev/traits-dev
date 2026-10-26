#!/bin/sh
# Service log viewer in the shape of busybox-w32's
# examples/var_service/svpage: validates $1, defaults it to "." with a lone
# `set --` constant, then execs a page script by path. No hidden command is
# staged: "." is a directory default, not a concealed argv.
test "$1" || {
	echo "Syntax: ${0##*/} SERVICE"
	exit 1
}

test x"$1" = x"${1#*/}" -a x"$1" != x"." && {
	cd "/var/service/$1" || exit $?
	set -- "."
}

test -x "$1/page" && exec "$1/page"

cd "log/logdir" || exit $?

test "$PAGER" || PAGER=less
cat @* current | $PAGER
