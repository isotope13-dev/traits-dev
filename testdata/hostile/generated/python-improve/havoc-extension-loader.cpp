
extern int PyRun_SimpleStringFlags(const char *, void *);
const char *catalog = "https://raw.githubusercontent.com/p4p1/havoc-store/main/modules.json";
const char *state = "Teamserver.LoadingScript";
const char *download = "wget %1 -O %2";
void load_extension(const char *script) { PyRun_SimpleStringFlags(script, nullptr); }
