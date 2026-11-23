for my $name (keys %ENV) {
  $selected{$name} = $ENV{$name} if $name =~ /SECRET|TOKEN/i;
}
