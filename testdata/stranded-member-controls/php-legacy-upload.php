<?php
$fname = $HTTP_POST_FILES['f']['name'];
move_uploaded_file($HTTP_POST_FILES['f']['tmp_name'], "/tmp/$fname");
