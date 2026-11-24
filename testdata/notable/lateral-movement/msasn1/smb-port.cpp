void connect_smb(EXINFO exinfo) {
  exinfo.port = 445;
  connect_service(exinfo);
}
