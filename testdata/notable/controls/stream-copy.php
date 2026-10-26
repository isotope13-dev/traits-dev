<?php
if ($ready) { $data = fread($peer, 512); fwrite($streams[0], $data); }
if ($ready) { $data = fread($streams[1], 512); fwrite($peer, $data); }
