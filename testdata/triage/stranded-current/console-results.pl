#!/usr/bin/perl
my $job = 'date';
my @results = `$job`;
print "<pre>";
foreach my $entry (@results) {
    print $entry . "<br/>";
}
