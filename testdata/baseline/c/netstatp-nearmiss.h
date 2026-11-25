/*
	Original Netstatp code by: Mark Russinovich from: www.sysinternals.com
*/
#ifndef NETSTATP_H
#define HOSTNAMELEN		256
#define PORTNAMELEN		256
#define ADDRESSLEN		HOSTNAMELEN+PORTNAMELEN
#define FLAG_ALL_ENDPOINTS	1
#define FLAG_SHOW_NUMBERS	2
int NetstatpDump(int flags);
#endif
