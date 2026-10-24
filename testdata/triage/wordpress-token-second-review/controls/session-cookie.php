<?php
wp_set_auth_cookie($id, false, is_ssl());
wp_set_auth_cookie($id);
wp_set_auth_cookie($id, $remember);
// wp_set_auth_cookie($id, true);
$documentation = "wp_set_auth_cookie($id, true)";
