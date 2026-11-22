#!/bin/sh
. ./test-lib.sh
test_expect_success 'credential reader' '
 cat ~/.netrc
'
test_done
