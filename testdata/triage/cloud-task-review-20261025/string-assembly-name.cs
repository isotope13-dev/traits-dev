using System.Reflection;
class LocalPlugin {
  static void Main(string[] args) {
    string name = "Approved.Plugin";
    Assembly.Load(name).GetType("Approved.Entry");
  }
}
