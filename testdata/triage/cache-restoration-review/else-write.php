<?php
if (!file_exists($cache)) {
    echo 'missing cache';
} else {
    file_put_contents($cache, 'replacement');
}
