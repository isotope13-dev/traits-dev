use Sys::Hostname qw(hostname);
sub log_host {
    print "build host\n" if (hostname() // '') =~ /^BUILD-/;
    return 1;
}
