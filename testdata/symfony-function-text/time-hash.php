<?php
function buildCacheId($hash, $time)
{
    return hash('crc32', $hash.$time);
}
