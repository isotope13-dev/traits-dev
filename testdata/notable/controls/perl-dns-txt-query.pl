use strict;
use warnings;

sub query_txt {
    my ($name) = @_;
    return qx{nslookup -type=TXT $name};
}
