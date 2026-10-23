#!/usr/bin/perl
use strict;
my $request = $ENV{QUERY_STRING};
$request =~ s/%20/ /g;
$request =~ s/%3b/;/g;
print "Content-type: text/plain\n\n";
print $request;
