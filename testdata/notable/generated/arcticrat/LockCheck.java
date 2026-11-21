class LockCheck { void check(String old) throws Exception {
 Runtime.getRuntime().exec("locksettings verify --old " + old);
} }
