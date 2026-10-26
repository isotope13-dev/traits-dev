const form = new FormData();
form.append("pluginzip", new Blob(["data"], {type: "application/zip"}));
fetch("/wp-admin/update.php?action=upload-plugin", {method: "POST", body: form});
