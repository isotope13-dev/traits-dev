<?php
if (!file_exists($input)) {
    file_put_contents($log, 'missing input');
}
