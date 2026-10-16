#!/bin/bash
exec 3<>/dev/tcp/10.0.0.1/4444
printf ping >&3
