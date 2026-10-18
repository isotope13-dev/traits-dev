#!/usr/bin/perl
print "Content-type: text/html\n\n";
my $query = $ENV{QUERY_STRING};
my $job = 'date';
my @results = `$job`;
print "<pre>";
foreach my $entry (@results) {
    print $entry . "<br/>";
}
