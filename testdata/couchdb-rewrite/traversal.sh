#!/bin/sh
curl --path-as-is -X OPTIONS 'http://127.0.0.1:5984/../../sampledb/_design/routes/_rewrite' -H 'Authorization: Basic YWRtaW46YWRtaW4='
