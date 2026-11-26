# Process injection walkthrough

This tutorial shows how to execute shellcode in a remote process on Windows.
Call CreateRemoteThread after writing the payload into the target.

Pick the target with a process identifier: pass the -pid value as a command line flag.
