using System.Net.Security;
using System.Security.Cryptography.X509Certificates;

namespace Sample.Clients
{
    public class ClientSettings
    {
        public bool AcceptInvalidCertificates { get; set; } = false;
    }

    public class SampleClient
    {
        private static bool AcceptCertificate(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors)
        {
            return true;
        }

        public void Connect(ClientSettings settings)
        {
            if (settings.AcceptInvalidCertificates)
            {
                ServicePointManager.ServerCertificateValidationCallback = (sender, certificate, chain, sslPolicyErrors) => true;
            }
        }
    }
}
