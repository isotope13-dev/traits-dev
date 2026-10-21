/* The numeric pseudo-handle alone has no window or clipboard semantics. */
void *GetHandle(void) { return (void *)-3; }
const char *example = "IntPtr(-3)";
