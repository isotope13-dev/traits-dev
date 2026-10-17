# dotnet worker host discovery

Managed tools that bootstrap an isolated `dotnet` worker process read
`DOTNET_HOST_PATH` (and `DOTNET_ROOT`) to locate the host before
launching the child. Those reads satisfy the profiling-environment leg
of `dotnet-profiler-anti-debug`, so the composite convicted benign
worker launchers such as AiDotNet.Evolution.Ptx (which writes an
embedded worker DLL plus its `.runtimeconfig.json` and execs it via
`FindDotnetHost`, with no profiler reaction, no debugger check, and no
self-kill).

`micro-behaviors/os/env/platform::dotnet-host-path-env-name` marks the
discovery read; the profiler composite skips files carrying it. The
atom stays notable so host discovery remains observable, and the
composite still convicts profiler checks without host discovery.

## Controls

`verify.py` builds three minimal PE32 fixtures and scans them with
`cleave --traits-dir`:

- `profiler-check-positive.exe`: `COR_ENABLE_PROFILING` plus
  `GetEnvironmentVariable` with no host discovery. Must report
  `dotnet-profiler-anti-debug`.
- `profiler-worker-negative.exe`: the positive plus `DOTNET_HOST_PATH`,
  `DOTNET_ROOT`, and `FindDotnetHost`. Must not report the hostile but
  must report `dotnet-host-path-env-name`.
- `host-discovery-only.exe`: host-path marker without profiling
  strings. Must report the atom and no hostile.
