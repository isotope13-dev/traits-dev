use strict;
use warnings;

sub start_worker {
    my $pid = fork();
    return $pid;
}

sub start_bare_worker {
    return fork;
}

sub start_core_worker {
    return CORE::fork();
}
