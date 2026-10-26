use strict;
use warnings;
use HTTP::Tiny;

# $http->post('https://example.invalid/status', { content => 'ready' });
my $example = q{$http->post('https://example.invalid/status', {})};

sub dispatch {
    my ($client, $method) = @_;
    return $client->$method('https://example.invalid/status', {});
}
