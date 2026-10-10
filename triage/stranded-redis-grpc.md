# Stranded Redis and gRPC members

The two enclosing archives remain confirmed malicious. These judgements apply
only to the 22 explicitly listed stranded members, each examined independently.
The dependency and other-member findings in the request are archive context,
not evidence against these members.

`atomscan --no-update <member>` and `cleave facts <member>` were run for every
member; final `atomscan --no-update --format json <member>` scans used this
worktree through `CLEAVE_TRAITS_DIR`. All final member scans contain **zero
hostile and zero suspicious traits**. The supplied hashes match the bytes.

All members are plain Go source. Source review covered imports, functions,
global initializers, call arguments, test fixtures and control flow. The Redis
examples connect to localhost and exercise data structures; FLUSHDB/DEL are
explicit fixture cleanup. Benchmarks exercise concurrency and local Redis
clusters. Auth tests use synthetic credentials and channel-based mock updates;
the command recorder stores a bounded history in memory. Protocol tests create
and parse memory buffers, including malformed RESP inputs. Numeric tests check
conversion results. The gRPC leak checker captures this process's goroutine
stacks and filters runtime/test workers; it does not detect a sandbox. Load and
throttle tests exercise counters, mocks and concurrency. Logging exits on fatal
errors; channelz IDs and resolver maps manipulate local data structures.

Facts contain no initialization HTTP or payload-flow events. Incidental
Base64 decodes of `expectedUser` and `MigratedSlot` are lexical coincidences,
not encoded payloads; the JSON tutorial's Unicode escapes are punctuation in
bike descriptions. Scans report `flow-graph-limited`; direct source review,
rather than the absence of flow events alone, supports the judgements. No
sample code was executed. Native disassembly is inapplicable to these source
members.

## Individual results

Risk is the final scanner score, not the member judgement.

| Member | Identity | Judgement | Risk | SHA-256 |
|---|---|---|---:|---|
| `bench_test.go` | Redis benchmark suite | BENIGN | 5 | `1647fa47e63ca2cbeec77e8cb3288893ce365469930816f66db5dc2f775295c8` |
| `auth/auth_test.go` | Redis streaming-auth unit tests | BENIGN | 3 | `a8c84ac8c2b0e903d4e779200c6951eceb8d0639404856f5ddd0efa79aa4e4c5` |
| `doctests/tdigest_tutorial_test.go` | Redis t-digest tutorial | BENIGN | 2 | `fd3bfe666aaf1f5b90501a20009442fd8faffae3b63d9f22df5bc9235e4a7146` |
| `doctests/json_tutorial_test.go` | Redis JSON tutorial | BENIGN | 2 | `e00499474dd5b18f9fef0c0cf5904987b6aa521cfd29dfe9f99f3bf9f0b931ff` |
| `doctests/ss_tutorial_test.go` | Redis sorted-set tutorial | BENIGN | 2 | `9c6da206e53ecf916a6a1820cc5744c3fea1352bd467d2b44ef42729dfc8c610` |
| `internal/proto/peek_push_notification_test.go` | Redis RESP3 push parser tests | BENIGN | 2 | `246c258898ae8e761b59f371da2c238effb97cdd568bcbfa8e39030878fa62c3` |
| `doctests/hash_tutorial_test.go` | Redis hash tutorial | BENIGN | 2 | `ded14cc7bebb537ef64565ff71eea9bafed406a68ef0afa6d44449e801db4a1c` |
| `doctests/list_tutorial_test.go` | Redis list tutorial | BENIGN | 2 | `7c96be64dddee11909ec2772a61de1d731d32af97fdf27a7bcc25c758b4edabd` |
| `internal/proto/writer_test.go` | Redis RESP writer tests | BENIGN | 2 | `6df278e48eed8a4f6bccca5cadcfc1b11830e22b40c14caf4af573fab7e74fcc` |
| `doctests/string_example_test.go` | Redis string examples | BENIGN | 2 | `6caef67a8c1e53f77413717f798262189833a1bda971b437700c5863273a845c` |
| `doctests/cmds_generic_test.go` | Redis key expiry examples | BENIGN | 2 | `637f5bae7456b12d1b2974d8314648f74e979fe026a025f4f1d973d36e81404f` |
| `doctests/sets_example_test.go` | Redis set examples | BENIGN | 2 | `2c18d9abaa0881e54652bd400cdb045f9562d842cf1c190b2cdac5de5514f3e4` |
| `doctests/cmds_list_test.go` | Redis list command examples | BENIGN | 2 | `22fecc63b90f56d5562814c1ea7239ce3f6b9016be0e88b7f21210a0bd32b38a` |
| `command_recorder_test.go` | Redis command recording test helper | BENIGN | 2 | `126517b7d8116e416cbec9e341ffd0d34301658e63a780f5a14f572e063d81d3` |
| `doctests/cmds_sorted_set_test.go` | Redis sorted-set command examples | BENIGN | 2 | `1121681b1808dd0b9c779938c6e5f76fcadb21c74e8e97128c73ec1607641123` |
| `internal/util/strconv_test.go` | Redis numeric conversion unit tests | BENIGN | 1 | `01625a551c67ee53c68f5699d9226e3ab267d03c6ebacc060a255039546f094e` |
| `internal/leakcheck/leakcheck.go` | gRPC goroutine leak checker | BENIGN | 4 | `f30d430a8f07d9495e1279ef2a346ab6a6f3439336ab1445d73d85275f4f723f` |
| `xds/internal/xdsclient/load/store_test.go` | gRPC load store unit tests | BENIGN | 3 | `d8f284f05812250dd9a8c737a1a0ccfeb9f782645c9f4d0ed42cbcf05cf1f26a` |
| `balancer/rls/internal/adaptive/adaptive_test.go` | gRPC adaptive throttle unit tests | BENIGN | 4 | `09a99f873ac3cc140b568c5cec1923524a3931bd56c1cdc726a3926c90d2571b` |
| `internal/grpclog/grpclog.go` | gRPC logging helper | BENIGN | 2 | `027874dfd77ce0279116f9887abd3f63474c186313d1e0b253c095b773f0a21d` |
| `internal/channelz/id.go` | gRPC channelz identifier helper | BENIGN | 2 | `aaf629d7d83a519a3fefaa6f90cd0b438591ad84a7651d33cc74c374381ea785` |
| `resolver/map.go` | gRPC resolver address map helper | BENIGN | 1 | `461ff7174800f7a9ee34550a46c68c349802e81c5cd48d79ea9b24590931f900` |

## Trait correction and migration audit

- Consolidated `well-known/lib/network/grpc-go::{authors-copyright,
  core-native-copyright}` and the Ruby `extconf-apache-header` into
  `metadata/package/license::grpc-authors-copyright`. Copyright survives forks
  and vendoring and proves neither an official Go library nor a Ruby gem.
  The description claims only the notice's author text. Criticality remains
  notable; the regex is unchanged for the Go/native predicates. Ruby scope
  admits all notice years instead of only 2015. Native size bounds were removed
  because the notice property is independent of file size.
- Removed `grpc-go::module-archive-path`: a versioned directory name alone does
  not establish implementation identity. No package-name allowlist or benign
  suppression was added. Removed these weak alternatives from both identity
  composites; retained the independent module/script/native loader indicators.
- Exact copyright references also appeared as extconf suppressors. Removed
  those notice-only suppressors: a copied header must not hide helper loading
  or child creation. Both neutral capabilities now remain visible. Ancestor
  selectors were reviewed: `metadata/binary/provenance/build` excludes the
  `well-known/lib` subtree, so eliminating false identity also eliminates that
  unsupported exclusion. The `metadata/package/license` downgrade consumer in
  token manipulation keeps its existing property meaning; no capability is
  hidden in these Go members. No proximity/needs threshold receives new legs.
- Controls in `testdata/stranded-grpc-provenance` cover copied copyright in Go,
  C and Ruby, unrelated copyright, a path-only module directory, the native
  Ruby loader, and an extconf helper/child invocation with a copied header. Headers yield only the new notice metadata; unrelated/path-only
  code has no gRPC identity. The native Ruby loader identity remains detectable.

Each judgement marker is next to its extracted member, outside the traits
repository; its one-line contents are preserved verbatim in the commit body.
