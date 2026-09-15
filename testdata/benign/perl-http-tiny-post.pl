use strict;
use warnings;
use HTTP::Tiny;

sub report_status {
    my $http = HTTP::Tiny->new();
    return $http->post(
        'https://example.invalid/status',
        { content => 'status=ready' },
    );
}
