for my $name (keys %ENV) {
  $selected{$name} = $ENV{$name} if $name =~ /LANG|TERM/i;
}
my $config = ".cpan/Config.pm";
