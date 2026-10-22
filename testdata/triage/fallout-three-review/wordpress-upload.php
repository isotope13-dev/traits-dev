<?php
check_admin_referer('upload');
$file = wp_handle_upload($_FILES['file'], array('test_form' => false));
