#!/bin/sh
openssl rand -hex 32
openssl enc -aes-256-cbc -in input -out encrypted -pass file:key
openssl pkeyutl -encrypt -pubin -inkey public.pem -in key -out wrapped
curl --data-binary @encrypted https://example.invalid/receive
