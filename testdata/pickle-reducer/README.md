Executable pickle reducer fixtures
==================================

`variant.py` must match `objectives/execution/interpreter/pickle::executable-reducer` and `executable-pickle-multipart-send`. It varies the method, execution callable, command, object name, and socket name from the LMCache advisory.

`benign.py` and `unrelated.py` must match neither objective. They distinguish ordinary object reconstruction and an execution callable returned outside the reducer. Fixtures are inspected statically; do not execute them.

Source: https://research.jfrog.com/vulnerabilities/lmcache-is-vulnerable-to-unauthenticated-remote-code-execution-via-pickle-deserialization-on-the-multiprocess-zmq-transport-cve-2026-105192-jfsa-2026-001694382/

Both objectives remain suspicious: the first identifies an executable reconstruction recipe; the second reports co-occurrence, rather than claiming proven data flow or successful remote execution. No LMCache, MessagePack extension number, endpoint, or command marker is required.
