<?php
// Schedules an hourly WordPress event that refreshes cached statistics.
function install_refresh( $hook ) {
	if ( ! wp_next_scheduled( $hook ) ) {
		wp_schedule_event( time(), 'hourly', $hook );
	}
	add_action( $hook, function () {
		update_option( 'stats_refreshed_at', time() );
	} );
}
