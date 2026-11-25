/* Minimal WinPcap capture loop: open an adapter, read one frame. */
#include <stdio.h>
#include <packet32.h>

int capture_one_frame(const char *adapter_name, char *buffer, UINT length)
{
    LPADAPTER adapter = PacketOpenAdapter((PCHAR)adapter_name);
    LPPACKET packet;

    if (adapter == NULL)
        return -1;
    packet = PacketAllocatePacket();
    if (packet == NULL)
        return -1;
    PacketInitPacket(packet, buffer, length);
    if (!PacketReceivePacket(adapter, packet, TRUE))
        return -1;
    PacketFreePacket(packet);
    PacketCloseAdapter(adapter);
    return 0;
}
