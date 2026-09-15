use strict;
use warnings;

my $command_example = 'nslookup -type=TXT example.invalid';
my $quoted_example = q{qx{nslookup -type=TXT example.invalid}};
# my $response = `nslookup -type=TXT example.invalid`;

sub query_address {
    return qx{nslookup -type=A example.invalid};
}
