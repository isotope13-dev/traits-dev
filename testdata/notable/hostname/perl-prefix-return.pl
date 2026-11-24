use Sys::Hostname qw(hostname);
sub selected_host {
    return 0 unless (hostname() // '') =~ /^BUILD-/;
    return 1;
}
