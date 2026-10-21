use IPC::Open3;
my $pid = open3($in, $out, undef, '/usr/bin/printf', '%s', $value);
waitpid($pid, 0);
