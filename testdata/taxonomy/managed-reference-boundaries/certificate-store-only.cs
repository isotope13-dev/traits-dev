using System.Security.Cryptography.X509Certificates;
class CertificateReader {
    void Open() {
        var store = new X509Store();
        store.Open(OpenFlags.ReadOnly);
    }
}
