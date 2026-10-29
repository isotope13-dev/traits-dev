#!/bin/sh
curl --request POST http://127.0.0.1:8080/api/mcp/client --data '{"connection_type":"stdio","stdio_config":{"command":"/bin/sh","args":["-c","printf ready"]}}'
