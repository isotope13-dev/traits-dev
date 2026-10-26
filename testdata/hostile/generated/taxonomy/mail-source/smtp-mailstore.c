const char *sender = "MAIL FROM:<analyst@example.invalid>";
const char *filter_name = "nospam_domains";
unsigned short smtp_port(void) { return htons(25); }
int looks_like_email(const char *s) { return s != 0; }
const char *mailboxes[] = {"/var/mail", "/var/spool/mail", "/home/user/.thunderbird/"};
