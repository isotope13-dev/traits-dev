-- Static control: the service name is not an argument to shell execution.
set serviceName to "Chrome Safe Storage"
display dialog serviceName
do shell script "whoami"
