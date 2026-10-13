<?php
// Minimized snapshot/restore integrity monitor: snapshots carry a .snap.php
// suffix, restores write snapshot bytes back, and the restore is reported.
// The touch/filemtime/chmod legs co-occur as declared recovery bookkeeping,
// so the stealth-rewrite composite must stay quiet via the restore context.
class Snapshot_Watchdog {
	const SNAP_SUFFIX = '.snap.php';

	public static function snapshot_file( $basename ) {
		$live = ABSPATH . $basename;
		$snap = self::snapshot_path( $basename );
		$content = @file_get_contents( $live );
		if ( false === @file_put_contents( $snap, $content, LOCK_EX ) ) {
			return false;
		}
		@touch( $snap, filemtime( $live ) );
		return true;
	}

	public static function restore( $basename, $original ) {
		$live = ABSPATH . $basename;
		$mtime = @filemtime( $live );
		$mode = @fileperms( $live );
		if ( is_file( $live ) ) {
			@chmod( $live, 0644 );
		}
		$ok = false !== @file_put_contents( $live, $original, LOCK_EX );
		@chmod( $live, 0444 );
		error_log( 'restored from snapshot: ' . $basename );
		return $ok;
	}

	private static function snapshot_path( $basename ) {
		return '/snapshots/' . $basename . self::SNAP_SUFFIX;
	}
}
