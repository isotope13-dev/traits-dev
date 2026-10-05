#!/bin/sh
ssh -o PermitLocalCommand=yes -o 'LocalCommand=sh -c "printf connected"' backup@backup.example
