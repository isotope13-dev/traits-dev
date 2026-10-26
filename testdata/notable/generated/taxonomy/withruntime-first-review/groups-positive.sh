#!/bin/sh
usermod -aG sudo alice
usermod -a -G users,wheel bob
