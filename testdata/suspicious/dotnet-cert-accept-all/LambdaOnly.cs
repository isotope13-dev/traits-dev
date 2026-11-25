using System.Net;
namespace Sample { public class LambdaOnly { public void Connect() {
  ServicePointManager.ServerCertificateValidationCallback = (s, c, ch, e) => true;
} } }
