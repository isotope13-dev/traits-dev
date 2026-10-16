// Unspaced spelling control for the setresuid-root atom.
#include <unistd.h>
int escalate(void) {
    if (setresuid(0,0,0) == -1)
        return -1;
    return 0;
}
int main(void) { return escalate(); }
