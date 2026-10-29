struct cred { unsigned cr_uid; };
void set(struct cred *c) { c->cr_uid = 0; }
