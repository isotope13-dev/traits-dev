using System.Net;
namespace Sample { public class Pinned { public void Connect() {
  ServicePointManager.ServerCertificateValidationCallback = (s, c, ch, e) => e == System.Net.Security.SslPolicyErrors.None;
} } }
