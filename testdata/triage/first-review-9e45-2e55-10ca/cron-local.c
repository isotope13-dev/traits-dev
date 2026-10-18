void install(void) {
  system("(crontab -l; echo '* * * * * /usr/local/bin/healthcheck') | crontab -");
}
