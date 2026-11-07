<?php
function mask_and_sort($rows, $hexMask) {
    ob_start();
    $order = $_GET['order'] ?? 'asc';
    assert(is_string($hexMask));
    assert(strlen($hexMask) > 0);
    $mask = pack('H*', $hexMask) ^ "\xff\xff\xff\xff";
    uasort($rows, "strnatcmp");
    usort($rows, function ($a, $b) { return strcmp($a, $b); });
    usort($rows, fn($a, $b) => $a <=> $b);
    return [$mask, $order, ob_get_clean()];
}
