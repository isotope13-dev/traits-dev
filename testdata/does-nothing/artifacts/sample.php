<?php

declare(strict_types=1);

function sample_log(string $message): void
{
    error_log(sprintf('[info] %s', $message));
}

sample_log('this sample does nothing');
