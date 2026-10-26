@echo off
java.exe -Dcom.sun.jndi.ldap.object.trustURLCodebase=true Lookup %*
