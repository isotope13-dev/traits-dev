using System;
using System.Reflection;
class ChangedNames {
    static void Replace(MulticastDelegate target, Delegate replacement) {
        FieldInfo storage = typeof(MulticastDelegate).GetField("_invocationList", BindingFlags.NonPublic | BindingFlags.Instance);
        object[] entries = (object[])storage.GetValue(target);
        entries[1] = replacement;
        storage.SetValue(target, entries);
    }
}
