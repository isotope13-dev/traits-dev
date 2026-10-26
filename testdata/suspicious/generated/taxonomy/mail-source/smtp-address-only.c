const char *sender = "MAIL FROM:<analyst@example.invalid>";
const char *filter_name = "nospam_domains";
unsigned short smtp_port(void) { return htons(25); }
