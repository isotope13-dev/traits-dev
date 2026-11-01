<?php
curl_setopt($handle, CURLOPT_POSTFIELDS, json_encode(array("server" => $_SERVER)));
