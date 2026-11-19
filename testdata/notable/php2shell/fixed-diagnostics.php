<?php
$data = base64_decode($_POST['record']);
$cmd = 'uptime';
system($cmd);
move_uploaded_file($_FILES['photo']['tmp_name'], '/var/tmp/image.jpg');
