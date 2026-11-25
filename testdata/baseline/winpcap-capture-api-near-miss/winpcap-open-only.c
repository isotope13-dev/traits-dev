/* Adapter probe: opens the named WinPcap adapter and reports success.
 * Frames are read elsewhere; PacketReceivePacket is not called here. */
#include <stdio.h>
#include <packet32.h>

int adapter_present(const char *adapter_name)
{
    LPADAPTER adapter = PacketOpenAdapter((PCHAR)adapter_name);

    if (adapter == NULL)
        return 0;
    PacketCloseAdapter(adapter);
    return 1;
}
