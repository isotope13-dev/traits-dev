// Firebird service API control: isc_action_svc_backup is the backup
// service action constant, not a backdoor account name, so the native
// backdoor user trait may not fire here.
#include "ifaceExamples.h"

int start_backup(IService* svc, IUtil* utl, ThrowStatusWrapper* status)
{
	IXpbBuilder* spb = utl->getXpbBuilder(status, IXpbBuilder::SPB_START, NULL, 0);
	spb->insertTag(status, isc_action_svc_backup);
	spb->insertString(status, isc_spb_dbname, "employee.fdb");
	spb->insertString(status, isc_spb_bkp_file, "employee.fbk");
	svc->start(status, spb->getBufferLength(status), spb->getBuffer(status));
	spb->dispose();
	return 0;
}
