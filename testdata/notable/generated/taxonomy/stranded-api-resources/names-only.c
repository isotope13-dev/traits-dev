const char *api_documentation[] = {
    "GetStdHandle", "SetStdHandle", "GetConsoleMode", "GetConsoleOutputCP"
};
void inspect_buffer(void) {
    unsigned char path[512];
    ReadDirectoryChangesW(path, 0, 0, 0, 0, 0, 0, 0);
}
