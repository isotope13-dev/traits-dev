#!/bin/sh
query="PREPARE report FROM @sql;
EXECUTE report;"
literal="PREPARE report FROM 'SELECT 1';"
printf '%s\n' "$query" "$literal"
