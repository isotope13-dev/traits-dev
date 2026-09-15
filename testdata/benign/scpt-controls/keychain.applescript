-- Static control: a keychain query without staging or transport.
do shell script "security find-generic-password -w -s 'Chrome Safe Storage'"
