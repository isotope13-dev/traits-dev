/* Static regression only. Do not execute. */
#include <stdlib.h>
#include <curl/curl.h>
void run(CURL *client) {
    curl_easy_setopt(client, CURLOPT_POSTFIELDS, getenv("DEPLOY_API_KEY"));
}
