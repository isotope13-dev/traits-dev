#!/bin/sh
ip xfrm state add src 192.0.2.1 dst 192.0.2.2 proto esp spi 256 mode transport
ip xfrm state list
