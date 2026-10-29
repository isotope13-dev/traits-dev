// Both forms identify procfs, rather than an arbitrary variable-root path.
const glob = '/proc/[0-9]*/cmdline';
const variablePid = '/proc/$worker/cmdline';
