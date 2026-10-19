using System.Security.Cryptography.X509Certificates;
class CertificateChooser {
    void Choose() {
        var store = new X509Store();
        store.Open(OpenFlags.ReadOnly);
        X509Certificate2UI.SelectFromCollection(store.Certificates,
            "Choose certificate", "Document signing", X509SelectionFlag.SingleSelection);
    }
}
