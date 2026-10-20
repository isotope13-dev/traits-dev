<?php
function cipher($data,$key) {return $data ^ $key;}
$input = $_POST['message'];
echo cipher($input,'key');
