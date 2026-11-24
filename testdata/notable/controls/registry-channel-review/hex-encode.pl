use strict;
use warnings;
my $encoded = unpack('H*', 'local data');
print $encoded;
