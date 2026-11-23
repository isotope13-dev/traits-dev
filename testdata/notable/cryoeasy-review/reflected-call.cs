using System;
class Plugin { public static void Run(Type t) { t.GetMethod("Refresh").Invoke(null, null); } }
