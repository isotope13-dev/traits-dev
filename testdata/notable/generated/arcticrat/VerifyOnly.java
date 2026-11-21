class VerifyOnly {
    void check(String credential) throws Exception {
        Runtime.getRuntime().exec(new String[]{"sh", "-c",
            "locksettings verify --old " + credential}).waitFor();
    }
}
