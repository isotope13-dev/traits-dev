#!/bin/sh
proxy --listen 0.0.0.0:8889 --upstream http://upstream:3000/mcp
