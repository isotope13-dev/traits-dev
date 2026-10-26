<?php
$cache = '/tmp/redirect-config';
if (filemtime($cache) < time()-30) {
 $raw = file_get_contents($config_url);
 $data = json_decode($raw, true);
 file_put_contents($cache, base64_encode($data['url']));
}
$target = base64_decode(file_get_contents($cache));
?><script>location.replace('<?php echo $target; ?>');</script>
