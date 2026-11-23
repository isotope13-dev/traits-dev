use File::Path qw(remove_tree);
remove_tree($_) for qw(/boot/grub2 /boot/grub /boot/efi);
