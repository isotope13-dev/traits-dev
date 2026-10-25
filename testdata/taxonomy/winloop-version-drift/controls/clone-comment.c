/* vfork() is equivalent to clone(CLONE_VM|CLONE_VFORK|SIGCHLD). */
int probe(void) { return vfork(); }
