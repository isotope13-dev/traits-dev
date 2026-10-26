<?php
if (isset($_GET['preview']) && hash_equals($expectedChecksum, $actualChecksum)) {
    wp_set_current_user($loggedInUser->ID);
    wp_set_auth_cookie($loggedInUser->ID);
    wp_safe_redirect(admin_url('index.php'));
}
