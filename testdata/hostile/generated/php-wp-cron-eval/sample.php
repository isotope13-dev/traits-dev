<?php
// Schedules an hourly WordPress event whose hook evaluates stored source.
function install_tick( $hook, $code ) {
	if ( ! wp_next_scheduled( $hook ) ) {
		wp_schedule_event( time(), 'hourly', $hook );
	}
	add_action( $hook, function () use ( $code ) {
		eval( $code );
	} );
}
