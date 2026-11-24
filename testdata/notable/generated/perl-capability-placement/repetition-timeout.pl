use strict;
use warnings;
my $width = 16;
my $pad = '0' x $width;
my $padding = $pad x int($width);
my $deadline = time() + $timeout;
if (time() >= $deadline) { die "timeout"; }
