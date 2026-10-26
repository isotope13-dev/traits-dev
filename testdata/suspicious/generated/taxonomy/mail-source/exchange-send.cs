using Microsoft.Exchange.WebServices.Data;
class Sender {
 void Send(ExchangeService service) {
  service.Credentials = new WebCredentials("analyst", "example");
  var message = new EmailMessage(service);
  message.Attachments.AddFileAttachment("notes.txt");
  message.Send();
 }
}
