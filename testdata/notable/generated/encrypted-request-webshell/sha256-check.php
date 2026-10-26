<?php
$expected = 'abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789';
if (hash('sha256', $_POST['token']) === $expected) { echo 'ok'; }
