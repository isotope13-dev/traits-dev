using System.IO;
class KeyDisplay { void OnKey(int vk) { File.AppendAllText("shortcut.log", ((Keys)vk).ToString()); } }
