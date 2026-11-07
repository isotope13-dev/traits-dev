<?php
header('Content-Disposition: attachment; filename="data"');
@readfile(urldecode($_GET['file']));
die();
