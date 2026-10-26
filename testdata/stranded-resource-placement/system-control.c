/* Compile-only benign control: a fixed message through the C shell API. */
extern int system(const char *);
int main(void) { return system("printf ok"); }
