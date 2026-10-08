<?php
// $_POST['password']; $_REQUEST['secret']; $_GET['api_key'];
// scandir('/'); readdir($dir); glob('*');
$dir = opendir('.');
move_uploaded_file($_FILES['file']['tmp_name'], '/tmp/upload');
?>
<form method="post" enctype="multipart/form-data"><input name="file" type="file"></form>
