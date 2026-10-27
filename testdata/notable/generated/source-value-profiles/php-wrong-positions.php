<?php
if ($ready) { $data = fread($peer, $streams[1]); fwrite($peer, $data); }
if ($ready) { $data = fread($streams[1], 512); fwrite($peer, "literal", $data); }
if ($ready) { $data = fread($peer, 512); fwrite($peer, "literal", $data); }
