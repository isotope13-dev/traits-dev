<?php
$users = get_users(['role' => 'editor']);
$example = "wp_insert_user(['role' => 'editor'])";
// wp_insert_user(['role' => 'editor']);
wp_insert_user(['role' => 'subscriber', 'description' => "'role' => 'editor'"]);
