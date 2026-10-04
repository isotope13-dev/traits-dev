import mmap
def region():
    return mmap.mmap(-1, 4096, prot=mmap.PROT_READ | mmap.PROT_EXEC)
