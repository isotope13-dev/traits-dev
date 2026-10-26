package paths
var raw = `\\.\PhysicalDrive0`
var escaped = "\\\\.\\Inspector"
var guid = `\\.\{12345678-abcd-1234-abcd-123456789abc}`
// Both observations: a regex elsewhere must not hide an actual device path.
var pattern = "[:\\\\.\\uFF0E]?[ \\u00A0\\\\t,-]*"
