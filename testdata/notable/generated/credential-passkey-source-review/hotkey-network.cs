using System.Net.Http;
class Hotkey { void Run() { if (GetAsyncKeyState(65) != 0) new HttpClient().PostAsync(url, status); } }
