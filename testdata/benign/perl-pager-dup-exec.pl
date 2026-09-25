#!/usr/bin/perl
# Benign control: the stock git pager idiom (pipe, fork, dup stdio onto the
# pipe ends, exec $pager). Duped stdio plus exec with no socket anywhere is
# a local pager, not a reverse shell.
use strict;
use warnings;

my $pager = $ENV{GIT_PAGER} || 'less';

sub run_pager {
    return unless defined $pager;
    pipe my ($rfd, $wfd) or return;
    defined(my $pid = fork) or die "Can't fork: $!";
    if (!$pid) {
        open STDOUT, '>&', $wfd or die "Can't redirect stdout: $!";
        return;
    }
    open STDIN, '<&', $rfd or die "Can't redirect stdin: $!";
    $ENV{LESS} ||= 'FRX';
    exec $pager or die "Can't run pager: $! ($pager)";
}

run_pager();
print "paged output\n";
