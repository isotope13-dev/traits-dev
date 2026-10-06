<?php
// Ordinary fatal error path: exits with a message variable, never a
// dynamically-dispatched call.
$db = connect_to_database();
if (!$db) {
    $message = "Could not connect, giving up.";
    die($message);
}
