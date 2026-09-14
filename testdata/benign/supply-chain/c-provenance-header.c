#include <stdlib.h>
#include <curl/curl.h>
void run(CURL *client) {
    curl_easy_setopt(client, CURLOPT_HTTPHEADER, getenv("DEPLOY_API_KEY"));
    curl_easy_setopt(client, CURLOPT_POSTFIELDS, "status");
}
