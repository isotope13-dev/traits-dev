use strict;
use warnings;
sub inspect_credentials {
    open my $in, '<', "$ENV{HOME}/.aws/credentials" or return;
    read $in, my $buffer, 32;
    print unpack('H*', $buffer);
}
sub check_dns {
    return gethostbyname('localhost');
}
sub is_odd {
    return $_[0] & 1;
}
