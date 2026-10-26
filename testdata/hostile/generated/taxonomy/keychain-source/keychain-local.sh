#!/bin/sh
security dump-keychain -d login
security find-generic-password
security find-internet-password
