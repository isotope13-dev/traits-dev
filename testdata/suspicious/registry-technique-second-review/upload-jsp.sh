#!/bin/sh
printf '%s\n' '<% out.print("unique_53"); %>' > diagnostic.jsp
curl -F 'payload=@diagnostic.jsp' https://audit.example.net/upload | grep unique_53
