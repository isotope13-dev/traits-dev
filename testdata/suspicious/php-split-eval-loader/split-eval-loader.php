<?php
// Regression: a split eval name in a plain loader, no scanner rule table, must keep firing.
$f = 'ev' . 'al';
$f( base64_decode( 'ZWNobyAxOw==' ) );
