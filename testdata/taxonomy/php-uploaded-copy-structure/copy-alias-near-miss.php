<?php
$temporaryPath = $_FILES['upload']['tmp_name'];
copy($temporaryPath, '/srv/www/theme/plugin.php');
