void inspect_standard_streams_and_console(void) {
    void *out = GetStdHandle(-11);
    SetStdHandle(-11, out);
    unsigned mode = 0;
    GetConsoleMode(out, &mode);
    GetConsoleOutputCP();
    char path[512];
    GetTempPathA(sizeof(path), path);
}
