using System.IO;
class CookieStore {
    string PathFor(string home) => Path.Combine(home, "Library", "Application Support", "Google", "Chrome", "Default", "Cookies");
}
