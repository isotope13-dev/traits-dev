#!/bin/sh
printf '%s\n' hello > record.txt
curl --form 'attachment=@record.txt' https://backup.example.net/files | grep success
