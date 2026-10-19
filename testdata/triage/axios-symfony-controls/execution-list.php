<?php
foreach (['exec', 'shell_exec', 'proc_open'] as $fn) {
 if (function_exists($fn)) { $fn($command); }
}
