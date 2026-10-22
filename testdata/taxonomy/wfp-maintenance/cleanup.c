/* Ordinary filter maintenance is not security-product targeting. */
void cleanup(HANDLE engine, HANDLE iterator, UINT64 id, GUID *provider,
             HANDLE process) {
    FWPM_FILTER0 filter = {0};
    FWPM_PROVIDER0 registration = {0};
    filter.flags = FWPM_FILTER_FLAG_PERSISTENT;
    registration.flags = FWPM_PROVIDER_FLAG_PERSISTENT;
    FwpmFilterEnum0(engine, iterator, 1, &entries, &count);
    FwpmFilterDeleteById0(engine, id);
    FwpmProviderDeleteByKey0(engine, provider);
    QueryFullProcessImageNameW(process, 0, path, &length);
}
