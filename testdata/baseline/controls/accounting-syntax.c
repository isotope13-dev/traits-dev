#include <utmp.h>
#include <lastlog.h>
#include <sys/acct.h>
#include <utmpx.h>
#ifdef HAVE_LASTLOG_H
struct lastlog last;
#endif
#ifdef HAVE_UTMPX
struct utmpx entry;
#endif
#ifndef NO_ACCT
struct acct usage;
#endif
const char *path = _PATH_UTMP;
