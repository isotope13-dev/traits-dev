<?php
// Near miss: fetches a remote translation bundle and caches it on disk, but
// never launches anything.
function fetch_bundle(string $url, string $cacheFile): ?string
{
    $body = @file_get_contents($url);
    if ($body === false || strlen($body) < 50) {
        return null;
    }
    @file_put_contents($cacheFile, $body);
    return $body;
}
