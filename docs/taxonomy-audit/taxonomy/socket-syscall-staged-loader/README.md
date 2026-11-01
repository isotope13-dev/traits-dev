# Socket syscall and staged-loader review

The 80-rule socket syscall leaf was split by observed operation: creation,
connection, data transfer, server operations, generic syscall dispatch, and
combined operations. Address construction, address query and socket-option
rules moved to those subjects. Their match conditions and effective defaults
are unchanged. One Mirai composite selected the entire former leaf; a
component retains the exact union, including the four rules that now live
outside the syscall tree. The new syscall leaves contain 5–19 rules each.

The staged-loader review moved 16 Java, PE and Python rules. JAR flags, ZIP
prefixes, source names and filesystem paths describe their own subjects; Java
payload preparation and launch chains use their staging or spawn sinks. Where
the process target is unknown, `spawn/decrypted` describes the preparation
without assuming that the target is a native executable or a runtime. A
Base64/cipher/write combination and two hashed-receive PE combinations are
suspicious profiles rather than confirmed staged payloads. The Python
credential-storage combination is a profile because its many alternatives do
not each establish staging. Their match conditions remain intact; three
severities were reduced.

The broad hosts-file consumer retains its prior alternatives. Its
process-artifact directory selector presently covers exactly its old members
plus the migrated member; future additions require reviewing that consumer.
