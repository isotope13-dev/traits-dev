<?php
if ($ready) { $read = fread($peer, 512); fwrite($streams[0], $other); }
if ($ready) { $read = fread($streams[1], 512); fwrite($peer, $other); }
