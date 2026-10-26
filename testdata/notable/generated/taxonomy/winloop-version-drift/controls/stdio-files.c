void launch(void) {
 STARTUPINFOW si = {0};
 si.dwFlags = STARTF_USESTDHANDLES;
 si.hStdInput = nul;
 si.hStdOutput = file;
 si.hStdError = file;
 CreateProcessW(image, args, 0, 0, 1, 0, 0, 0, &si, &pi);
}
