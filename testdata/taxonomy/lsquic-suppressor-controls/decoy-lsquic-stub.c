/* Synthetic decoy library: exports only the symbol name used by the matcher. */
int lsquic_engine_connect(void *engine, const void *address, unsigned int address_len,
                          void *stream_if, void *connection_ctx) {
    (void)engine;
    (void)address;
    (void)address_len;
    (void)stream_if;
    (void)connection_ctx;
    return 0;
}
