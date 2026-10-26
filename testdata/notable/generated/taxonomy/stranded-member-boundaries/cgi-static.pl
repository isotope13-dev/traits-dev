#!/usr/bin/perl
use strict;
print "Content-type: text/html\n\n";
my $req = $ENV{QUERY_STRING};
my @cmd = `date`;
foreach my $line (@cmd) {
    print $line . "<br/>";
}
