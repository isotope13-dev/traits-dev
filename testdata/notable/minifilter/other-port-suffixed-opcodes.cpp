#include <windows.h>
#include <fltuser.h>
void request(HANDLE channel, void *buffer, DWORD size) {
    FilterConnectCommunicationPort(L"\\ExampleMonitorPort", 0, 0, 0, 0, &channel);
    struct Packet { BYTE Opcode; } packet;
    packet.Opcode = 0x0eUL;
    FilterSendMessage(channel, &packet, sizeof(packet), buffer, size, 0);
    packet.Opcode = 70u;
    FilterSendMessage(channel, &packet, sizeof(packet), buffer, size, 0);
}
