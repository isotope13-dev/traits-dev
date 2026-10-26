#!/bin/bash
if [[ "$HTTP_STATUS" =~ ^50[13]$ ]]; then eval "$HANDLER"; fi
