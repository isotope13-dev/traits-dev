<?php
$k = '550e8400-e29b-41d4-a716-446655440000';
$plain = $k ^ pack('H*', '11223344556677889900aabbccddeeff');
echo $plain;
