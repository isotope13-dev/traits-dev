const char *references[] = {
"#include <utmp.h>", "#include <lastlog.h>",
"#include <sys/acct.h>", "#include <utmpx.h>",
"#ifdef HAVE_LASTLOG_H", "#ifdef HAVE_UTMPX", "#ifndef NO_ACCT",
"_PATH_UTMP", "struct utmp", "struct lastlog"
};
