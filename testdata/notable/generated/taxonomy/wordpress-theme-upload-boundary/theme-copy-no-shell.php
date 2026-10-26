<?php
copy(
    $_FILES['theme']['tmp_name'],
    '/var/www/html/wp-content/themes/example/functions.php'
);
