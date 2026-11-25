#!/bin/sh -e

check_var_exists() {
  var="$1"
  val="$(eval echo "\$$var")"

  if [ -z "$val" ]; then
    echo "The $var variable is missing." >&2
    exit 1
  fi
}

check_var_exists "DEVELOPER_ID_CERT"
check_var_exists "DEVELOPER_ID_PASSWORD"
