/* mprotect(region, length, PROT_EXEC); socket(AF_INET, SOCK_DGRAM, 0); */
int mprotect(void *, unsigned long, int);
int socket(int, int, int);
unsigned int if_nametoindex(const char *);
const char *documentation = "mprotect(region, length, PROT_EXEC)";
void ordinary(void) { int result = 1; }
