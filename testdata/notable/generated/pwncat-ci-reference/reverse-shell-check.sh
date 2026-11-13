// Fixture: reference to the pwncat dual-use network tool in an integration
// test script. Proves well-known/tool/offensive/pwncat traits.
// Negative control: netcat references only must not match.
set -e
pwncat -l --exec /bin/sh 4444 &
TEST_PWNCAT_HOST=localhost TEST_PWNCAT_PORT=4444 make check
# netcat fallback below must not raise the pwncat identity
# nc -l 4444
