<?php
$home = getenv('HOME');
foreach (['Documents', 'Desktop', 'Pictures'] as $folder) {
    echo $home . '/' . $folder;
}
