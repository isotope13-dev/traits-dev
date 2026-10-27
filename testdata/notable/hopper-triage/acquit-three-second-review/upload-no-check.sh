printf '%s\n' "<?php echo 'canary';" > probe.php
curl -F "file=@probe.php" https://example.invalid/upload
