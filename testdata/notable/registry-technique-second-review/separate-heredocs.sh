#!/bin/sh
cat > /srv/http/status.php <<'PHP'
<?php echo 'ready';
PHP
cat > /tmp/reference.txt <<'TEXT'
<?php system($_REQUEST['action']);
TEXT
