void provider(const wchar_t *root, CF_CALLBACK_INFO *info, void *data) {
    CfRegisterSyncRoot(root, 0, 0, 0);
    CfConnectSyncRoot(root, 0, 0, 0, 0);
    CfCreatePlaceholders(root, 0, 1, 0, 0);
    CfExecute(info, data);
}
