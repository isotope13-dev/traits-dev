<?php
if (openssl_sign($data, $signature, $key)) { echo "ok"; }
