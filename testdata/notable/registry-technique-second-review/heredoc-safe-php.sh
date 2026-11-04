#!/bin/sh
cat > /srv/http/status.php <<'PHP'
<?php echo 'healthy';
PHP
