#!/bin/bash
if [[ "$HTTP_STATUS" == 401 || "$HTTP_STATUS" == 403 ]]; then echo "authentication rejected"; fi
