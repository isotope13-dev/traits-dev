// Detection regression fixture: a profiler reads a target's heap through
// ReadProcessMemory and reports byte counts. No session material is searched.
const PROFILER = `
public static class HeapProbe {
  [DllImport("kernel32.dll")] public static extern bool ReadProcessMemory(IntPtr h, IntPtr a, byte[] b, int n, out IntPtr r);
}`

export function heapSizeLabel(bytes) {
  return `${(bytes / 1024).toFixed(1)} KiB`
}

export { PROFILER }
