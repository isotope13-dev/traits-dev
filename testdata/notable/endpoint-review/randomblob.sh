#!/bin/sh
sqlite3 local.db "UPDATE records SET data=hex(randomblob(262144));"
