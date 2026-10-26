#!/bin/sh
java -Dcom.sun.jndi.rmi.object.trustURLCodebase=true Lookup "$@"
