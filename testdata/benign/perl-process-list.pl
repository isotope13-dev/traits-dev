use strict;
use warnings;

sub report_status {
    system 'printf', '%s', 'ready';
}

sub replace_status {
    exec 'printf', '%s', 'ready';
}
