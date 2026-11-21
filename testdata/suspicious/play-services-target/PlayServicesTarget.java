class PlayServicesTarget {
    void configure(android.net.VpnService.Builder builder) throws Exception {
        builder.addDisallowedApplication("com.google.android.gms");
    }
}
