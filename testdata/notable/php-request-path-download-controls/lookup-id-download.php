<?php
$id = (int) $_GET['id'];
$row = get_attachment_row($id);
$path = UPLOAD_DIR . '/' . $row['stored_name'];
header('Content-Disposition: attachment; filename="' . $row['original_name'] . '"');
readfile($path);
