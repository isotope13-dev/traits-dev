#!/bin/sh
for client in 04b07795-8ddb-461a-bbee-02f9e1bf7b46; do
  response=$(curl -X POST https://login.microsoftonline.com/common/oauth2/v2.0/token \
    -d "client_id=$client" -d "grant_type=refresh_token" -d "refresh_token=$TOKEN")
done
