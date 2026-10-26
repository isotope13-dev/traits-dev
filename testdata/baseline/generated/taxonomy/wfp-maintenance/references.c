/* FwpmFilterEnum0(engine, iterator, 1, &entries, &count); */
/* FwpmFilterDeleteById0(engine, id); */
/* FwpmProviderDeleteByKey0(engine, provider); */
/* QueryFullProcessImageNameW(process, 0, path, &length); */
void FwpmFilterDeleteById0(HANDLE engine, UINT64 id);
void QueryFullProcessImageNameW(HANDLE process, DWORD flags, void *out, void *size);
const char *documentation = "FwpmFilterEnum0() FwpmProviderDeleteByKey0()";
/* Similar names must not count as persistent filter/provider flag references. */
unsigned FWPM_FILTER_FLAG_PERSISTENT_TEST = 0;
unsigned FWPM_PROVIDER_FLAG_PERSISTENT_TEST = 0;
