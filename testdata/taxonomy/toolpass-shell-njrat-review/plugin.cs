using System;
using System.IO;
using System.Reflection;
class PluginHost {
  static void Load(string approvedPath) {
    var directory = Assembly.GetExecutingAssembly().Location;
    byte[] bytes = File.ReadAllBytes(approvedPath);
    var configuration = Convert.FromBase64String("dGVzdA==");
    Activator.CreateInstance(typeof(object));
  }
}
