#!/bin/sh
nvram set jffs2_scripts=1
nvram commit
printf '#!/bin/sh\nlogger WAN is up\n' > /jffs/scripts/wan-start
chmod +x /jffs/scripts/wan-start
