#!/bin/sh
printf '%s\n' '<% Response.Write("marker_9"); %>' > status.aspx
curl -F 'part=@status.aspx' https://audit.example.net/upload | grep marker_9
