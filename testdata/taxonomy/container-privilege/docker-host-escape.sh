#!/bin/sh
docker run --privileged -v /:/host alpine chroot /host /bin/sh
