use strict;
sub check_host {
    my ($base, $suffix) = @_;
    my $pid = fork();
    if ($pid == 0) {
        exec "ping", "-c", "1", "$base$suffix";
    }
}
