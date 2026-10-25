<?php
// Diagnostics and media import do not establish command execution.
echo php_uname();
if (isset($_FILES['media'])) {
    move_uploaded_file($_FILES['media']['tmp_name'], getcwd() . '/image.dat');
}
?>
<form method="post" enctype="multipart/form-data"><input type="file" name="media"></form>
