#!/bin/sh
      fcode=$(curl -sS --max-time 20 -o "$D/az_fic_add_$fi2.json" -w '%{http_code}' -X POST \
        -H "Authorization: Bearer $AGRAPH" -H "Content-Type: application/json" \
        -d "{\"name\":\"wfx-ci-$fi2\",\"issuer\":\"https://token.actions.githubusercontent.com\",\"subject\":\"$SUBJ\",\"audiences\":[\"api://AzureADTokenExchange\"]}" \
        "https://graph.microsoft.com/v1.0/applications/$oid/federatedIdentityCredentials" 2>>"$D/errors.log")
