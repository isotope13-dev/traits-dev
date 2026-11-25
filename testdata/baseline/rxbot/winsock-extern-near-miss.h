/* Standard WinSock wrapper declarations */
extern int WSAStartup_wrapper(void);
extern int socket_wrapper(int af, int type, int proto);
extern int connect_wrapper(int s, const void *name, int namelen);
