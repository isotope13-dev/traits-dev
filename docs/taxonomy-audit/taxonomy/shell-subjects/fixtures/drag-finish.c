#include <windows.h>
#include <shellapi.h>
int main(int argc, char **argv) { DragFinish((HDROP)(ULONG_PTR)argc); return 0; }
