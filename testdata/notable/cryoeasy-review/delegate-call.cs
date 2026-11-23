using System;
class Plugin { public static void Run(Action callback) { callback.Invoke(); } }
