const shell = new ActiveXObject("Shell.Application");
shell.NameSpace("C:\\tmp").ParseName("file.txt").ModifyDate = new Date();
reg.SetStringValue(HKEY_CURRENT_USER, "Software\\Example", "name", "value");
const target = ".cursor/rules/global.mdc";
