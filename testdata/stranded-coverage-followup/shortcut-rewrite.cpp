// Static technique fixture; never built or executed.
const char *shortcut_pattern = "*.lnk";
const auto shortcut_class = CLSID_ShellLink;
void rewrite(IShellLink &link) {
    link.SetPath("C:\\ProgramData\\relay.exe");
    link.SetArguments("original-target");
}
