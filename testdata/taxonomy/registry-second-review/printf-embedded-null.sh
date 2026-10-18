#!/bin/sh
printf '#!/bin/sh\ncurl -s https://remote.invalid/p >/dev/null 2>&1\n' \
  > /tmp/helper
