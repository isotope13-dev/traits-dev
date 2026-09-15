use strict;
use warnings;

my $documentation = <<'EXAMPLE';
system('printf', 'ready');
my $pid = fork();
exec 'printf', 'ready';
EXAMPLE

# system 'printf', 'ready';
# my $pid = fork();
# exec('printf', 'ready');
