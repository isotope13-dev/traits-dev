<?php
$dir = opendir('.');
$entry = readdir($dir);
$entries = scandir('.');
$iterator = new RecursiveDirectoryIterator('.');
