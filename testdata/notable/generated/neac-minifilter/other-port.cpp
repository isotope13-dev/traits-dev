#include <windows.h>
void notify(HANDLE port) {
 struct { int Opcode; } request;
 FilterConnectCommunicationPort(L"\\BackupMonitorPort", 0, 0, 0, 0, &port);
 request.Opcode = 14;
 FilterSendMessage(port, &request, sizeof(request), 0, 0, 0);
 request.Opcode = 70;
 FilterSendMessage(port, &request, sizeof(request), 0, 0, 0);
}
