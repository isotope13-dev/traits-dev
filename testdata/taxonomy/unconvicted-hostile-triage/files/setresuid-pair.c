// Escalation pair control: a root user-id request beside a group-side
// setter is the two-role pattern native-setresuid-escalation convicts,
// unlike the lone calls in setresuid-spaced.c / setresuid-unspaced.c.
#include <unistd.h>
int escalate(void) {
    if (setresuid(0, 0, 0) == -1)
        return -1;
    if (setresgid(0, 0, 0) == -1)
        return -1;
    return 0;
}
int main(void) { return escalate(); }
