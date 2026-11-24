use strict;
use warnings;
use File::Path qw(remove_tree);
sub cleanup_staging {
    my $home = '/tmp/export-staging';
    remove_tree("$home/$_") for qw(Documents Desktop Pictures);
}
1;
