<?php
$root = $_SERVER['DOCUMENT_ROOT'];
$dir = isset($_GET['dir']) ? $_GET['dir'] : $root;
if (isset($_FILES['up'])) { move_uploaded_file($_FILES['up']['tmp_name'], $dir . '/' . $_FILES['up']['name']); }
if (isset($_POST['rm'])) { unlink($_POST['rm']); }
foreach (scandir($dir) as $e) { echo "<a href='?dir=$dir/$e'>$e</a><br>"; }
if (isset($_GET['get'])) { $fid = intval($_GET['get']); $p = lookup($fid); header('Content-Disposition: attachment; filename="x"'); readfile($p); }
?>
<form method="post" enctype="multipart/form-data"><input type="file" name="up"></form>
