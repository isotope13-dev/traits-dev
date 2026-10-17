# Lease-holder bookkeeping: username travels as a URL query value.
curl -s -X POST "${HOST}/acquire?resource=${name}&owner=$(whoami)" | grep -q "${name}"
