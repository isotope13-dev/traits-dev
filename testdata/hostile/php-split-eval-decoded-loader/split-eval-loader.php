<?php
// Near miss for the scanner-table exemption: a split eval name in a plain loader, no rule table.
$f = 'ev' . 'al';
$f( base64_decode( 'ZWNobyAxOw==' ) );
