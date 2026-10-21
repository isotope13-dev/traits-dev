# Crypt::Rijndael->new($key); $cipher->encrypt($data); $cipher->decrypt($data);
use IPC::Open3;
my $manual = 'open3($in, $out, undef, "/usr/bin/printf")';
