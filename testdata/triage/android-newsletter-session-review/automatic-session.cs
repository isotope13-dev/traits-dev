using System;
class RemoteDelivery {
 private HashSet<string> delivered = new HashSet<string>();
 void OnStatus(ScreenConnect.EndPointStatusMessage message) {
   var active = new HashSet<string>();
   foreach (var connection in message.Connections) {
     if (connection.ProcessType.ToString() == "Host") {
       var id = connection.ConnectionID;
       active.Add(id);
       if (!delivered.Contains(connection.ConnectionID)) {
         var files = sender.RegisterVirtualFiles(ReadScriptBundle(), null);
         var outgoing = new ScreenConnect.TransferFilesMessage();
         outgoing.Files = files;
         outgoing.Action = ScreenConnect.FileAction.Run;
         client.EnqueueOutgoingMessage(outgoing);
         delivered.Add(id);
       }
     }
   }
   delivered.IntersectWith(active);
 }
}
