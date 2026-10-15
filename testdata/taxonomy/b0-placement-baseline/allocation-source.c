/* The baseline commit flags and executable-read mode support the composite. */
void allocate_buffer(void) {
    VirtualAlloc(0, 4096, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READ);
}
