void acl(EXPLICIT_ACCESSW *entry) {
    SID_IDENTIFIER_AUTHORITY unused = SECURITY_WORLD_SID_AUTHORITY;
    entry->grfAccessPermissions = GENERIC_ALL;
    SetEntriesInAclW(1, entry, 0, 0);
}
