<?php
/*
 * This file is part of the Symfony package.
 */
namespace Symfony\Component\Filesystem;
class MiniFilesystem
{
    public function copy($originFile, $targetFile)
    {
        $doCopy = filemtime($originFile) > filemtime($targetFile);
        if ($doCopy) {
            $source = @fopen($originFile, 'r');
            $target = @fopen($targetFile, 'w');
            stream_copy_to_stream($source, $target);
            @chmod($targetFile, fileperms($targetFile) | (fileperms($originFile) & 0111));
        }
    }
    public function touch($files, $time = null, $atime = null)
    {
        foreach ((array) $files as $file) {
            $touch = $time ? @touch($file, $time, $atime) : @touch($file);
        }
    }
    public function dumpFile($filename, $content)
    {
        file_put_contents($filename, $content);
    }
}
