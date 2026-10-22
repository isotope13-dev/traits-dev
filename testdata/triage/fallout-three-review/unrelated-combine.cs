using System.IO;
class Export {
    string PathFor(string home) => Path.Combine(home, "Chrome", "Exports");
    string label = "Cookies";
}
