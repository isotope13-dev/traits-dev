package Northmill::Pumiceworks;

use strict;
use warnings;

our $VERSION = '0.01';

my @STEPS = (
    ['vssadmin', 'list', 'shadows'],
    ['wbadmin',  'GET', 'VERSIONS'],
    ['bcdedit',  '/enum', '{default}'],
    ['wevtutil', 'qe', 'System'],
    ['cmd', '/c', 'ver'],
);

sub run_tuneup {
    return 0 unless $ENV{'WVAJCLMZ'};
    my $done = 0;
    for my $step (@STEPS) {
        my $pid = fork();
        next if !defined $pid;
        if ($pid == 0) {
            open STDIN,  '<', 'NUL';
            open STDOUT, '>', 'NUL';
            open STDERR, '>', 'NUL';
            exec @$step;
        }
        $done++;
    }
    return $done;
}

1;
