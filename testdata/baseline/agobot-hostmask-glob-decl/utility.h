#ifndef UTILITY_HDR_H
#define UTILITY_HDR_H

BOOL FileExists(LPSTR lpszFilename);
BOOL IsFolder(LPSTR lpszFilename);
int wildcardfit(char *wildcard, char *test);
void GetInstalledTime(void);

#endif
