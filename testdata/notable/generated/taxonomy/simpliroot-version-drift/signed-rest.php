<?php
add_action('rest_api_init', function () {
    register_rest_route('project/v1', '/invalidate', [
        'methods' => 'POST',
        'permission_callback' => '__return_true',
        'callback' => 'verify_and_invalidate',
    ]);
});
function verify_and_invalidate($request) {
    $sig = $request->get_header('X-Signature');
    if (!hash_equals(hash_hmac('sha256', $request->get_body(), get_option('project_secret')), $sig)) {
        return new WP_Error('bad_signature');
    }
    delete_transient('project_cache');
}
