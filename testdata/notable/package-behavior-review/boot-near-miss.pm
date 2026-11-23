use File::Path qw(remove_tree);
my $boot = "/boot/grub";
remove_tree("/tmp/cache");
