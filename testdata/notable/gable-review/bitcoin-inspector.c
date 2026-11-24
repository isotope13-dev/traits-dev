#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void inspect(const char *url) {
    char cmd[512], body[4096];
    snprintf(cmd, sizeof(cmd), "curl -fsSL '%s'", url);
    FILE *p = popen(cmd, "r");
    if (!p) return;
    fread(body, 1, sizeof(body)-1, p);
    puts(strstr(body, "op_return") ? "OP_RETURN present" : "none");
    pclose(p);
}
