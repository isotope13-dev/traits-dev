public class FalseTrust {
    static void configure() {
        System.setProperty("com.sun.jndi.ldap.object.trustURLCodebase", "false");
        System.setProperty("other.option", "true");
    }
}
