// Ordinarily formatted escalation stub: spaces after the commas. The
// setresuid-root atom must see through normal C formatting.
#include <unistd.h>
int escalate(void) {
    if (setresuid(0, 0, 0) == -1)
        return -1;
    return 0;
}
int main(void) { return escalate(); }
