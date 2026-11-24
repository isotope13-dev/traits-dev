// SPDX-License-Identifier: GPL-3.0-or-later
/* Regression: the SOAP parser must refuse an external entity declaration. */
#include <stdio.h>
#include <string.h>

static int check_refused(const char* body) {
    return strstr(body, "<!ENTITY") != NULL ? 0 : 1;
}

int main(void) {
    static const char k_doctype[] = "<?xml version=\"1.0\"?>"
                                    "<!DOCTYPE Envelope [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]>"
                                    "<Envelope><Body><return><username>&xxe;</username></return></Body></Envelope>";
    if (!check_refused(k_doctype)) {
        fprintf(stderr, "FAIL: external entity accepted\n");
        return 1;
    }
    return 0;
}
