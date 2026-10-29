void do_log(int quiet) { if (!quiet || quiet != 1) { syslog(1,"audit"); } }
