<?php
if (openssl_verify($data, $signature, $key)) { echo "ok"; }
