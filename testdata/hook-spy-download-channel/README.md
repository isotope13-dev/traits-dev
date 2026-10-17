Hook spy with a download channel instead of Winsock
====================================================

`hook-debugpriv-process-control-network-channel` convicts an unsigned
binary combining a window-hook lifecycle, SeDebugPrivilege-gated process
access, process termination, thread creation, and a network channel. The
channel leg used to require only the WSOCK32 marker, so hook-based
spyware reaching the network through a URLMon download
(`URLDownloadToFile`) escaped conviction while keeping the same
surveillance-and-control shape. The leg now accepts either channel.

Run `python3 testdata/hook-spy-download-channel/verify.py
<scratch-directory>`. Both positives (URLMon and WSOCK32 channels) must
report the hostile; removing the hook pair or every network leg must
not.
