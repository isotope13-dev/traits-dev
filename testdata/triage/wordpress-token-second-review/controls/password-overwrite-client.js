fetch('/wp-admin/admin-ajax.php?route=fixture', {
method: 'POST', headers: {'Accept': 'application/json'},
body: JSON.stringify({ action: 'pods_admin', method: 'save_user',
'meta-box-loader': '1', 'user_pass': password })
});
