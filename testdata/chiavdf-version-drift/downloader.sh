#!/bin/sh
fetch -o /tmp/result https://example.com/file
fetch https://example.com/file
result=$(fetch -q https://example.com/file)
