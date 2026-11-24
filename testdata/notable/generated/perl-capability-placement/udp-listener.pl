use IO::Socket::INET;
my $socket = IO::Socket::INET->new(LocalPort => 9999, Proto => 'udp');
my $message;
$socket->recv($message, 1024);
print $message;
