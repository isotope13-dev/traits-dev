using Microsoft.Exchange.WebServices.Data;
class Reader {
 void Read(ExchangeService service) {
  var folders = service.FindFolders(new FolderView(100));
  var items = service.FindItems(new ItemView(100));
  var content = items[0].MimeContent;
  var setterName = "set_ServerCertificateValidationCallback";
 }
}
