#!/usr/bin/env perl
use strict;
use warnings;
use feature qw(say);

sub log_info {
    my ($message) = @_;
    say STDERR "[info] $message";
}

log_info("this sample does nothing");
