#!/bin/bash
# Static analyzer control. Never install or publish this fixture.
# Build smoke test: an inline snippet is executed by the just-built local
# binary to verify it runs. Nothing is uploaded anywhere.
set -e
./sapi/cli/php -v
echo '<?php echo "Hello from PHP\n"; ?>' | ./sapi/cli/php
