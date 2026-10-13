using System;

class BrowserQuery
{
    void Query()
    {
        var history = @"C:\Users\Alice\AppData\Local\Google\Chrome\User Data\Default\History";
        var sql = "SELECT url, title, visit_count FROM urls WHERE url LIKE '%example.com%'";
        Console.WriteLine(Environment.ProcessPath);
    }
}
