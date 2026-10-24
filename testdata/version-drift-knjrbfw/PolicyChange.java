// Compile only: this fixture is never executed.
class PolicyChange {
    static final String GRANT = "permission java.security.AllPermission;";
    static void configure() {
        System.setSecurityManager(null);
        java.security.Security.setProperty("jdk.certpath.disabledAlgorithms", "");
    }
}
