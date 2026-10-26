<?php
// Classic anti-forensic rewrite: capture the victim's mode and mtime,
// overwrite it, then put both back. No snapshot machinery anywhere, so the
// stealth-rewrite composite must keep firing here.
function stealth_patch( $path, $payload ) {
	$mtime = @filemtime( $path );
	$mode = @fileperms( $path );
	@file_put_contents( $path, $payload, LOCK_EX );
	@chmod( $path, $mode );
	@touch( $path, $mtime );
	return true;
}
