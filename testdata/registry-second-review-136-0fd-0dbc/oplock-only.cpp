// Ordinary filesystem-cache coordination; no redirection or protected target.
void request(HANDLE file, void *input, void *output, OVERLAPPED *overlapped) {
    DeviceIoControl(file, FSCTL_REQUEST_OPLOCK, input, 0, output, 0, 0, overlapped);
}
