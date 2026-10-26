@echo off
rem java -Dcom.sun.jndi.ldap.object.trustURLCodebase=true Lookup
:: java -Dcom.sun.jndi.rmi.object.trustURLCodebase=true Lookup
java -Dcom.sun.jndi.ldap.object.trustURLCodebase=false Lookup
java -Dcom.sun.jndi.rmi.object.trustURLCodebase=true.suffix Lookup
