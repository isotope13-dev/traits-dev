struct cred { unsigned cr_uid; };
int check(struct cred *c) { return c->cr_uid == 0; }
