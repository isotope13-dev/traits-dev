use Crypt::Rijndael;
my $cipher = Crypt::Rijndael->new($key, Crypt::Rijndael::MODE_CBC());
my $backup = $cipher->encrypt($data);
my $restored = $cipher->decrypt($backup);
