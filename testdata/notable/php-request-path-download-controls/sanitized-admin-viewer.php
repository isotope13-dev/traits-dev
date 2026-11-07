<?php
class Report_Viewer {
    public function handle_view() {
        if (!current_user_can('manage_options')) {
            wp_die('Forbidden', 403);
        }
        $relative = isset($_GET['file']) ? $this->sanitize_relative(wp_unslash($_GET['file'])) : '';
        check_admin_referer('view_' . $relative);
        $absolute = $this->absolute_path($relative);
        header('Content-Disposition: inline; filename="' . sanitize_file_name(basename($relative)) . '"');
        readfile($absolute);
        exit;
    }
}
