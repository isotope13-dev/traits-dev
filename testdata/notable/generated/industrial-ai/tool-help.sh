#!/bin/sh
# nmap -sS 192.0.2.10
# nuclei -u http://192.0.2.10
# sqlmap -u http://192.0.2.10
# chisel client 192.0.2.20:8080 R:socks
printf '%s\n' 'sqlmap -u http://192.0.2.10' 'R:socks'
nmap --version
nuclei -version
sqlmap --version
chisel server --help
