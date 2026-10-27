<?php
if (!file_exists($dest)) {
    file_put_contents($dest, $contents);
}
include $dest;
