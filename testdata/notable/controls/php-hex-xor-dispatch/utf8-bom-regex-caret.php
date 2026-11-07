<?php
function remove_utf8_bom($text) {
    $bom = pack('H*', 'EFBBBF');
    return preg_replace("/^$bom/", '', $text);
}
$page = $_GET['page'] ?? 'home';
uasort($files, "sortVideosURL");
$arr = ['GET', 'POST'];
foreach ($arr as $v) { eval('$saved[$v] = $_' . $v . ';'); }
