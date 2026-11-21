class ConscryptClient {
    void configure(android.net.VpnService.Builder builder, String excluded) throws Exception {
        Class.forName("com.google.android.gms.org.conscrypt.SSLParametersImpl");
        builder.addDisallowedApplication(excluded);
    }
}
