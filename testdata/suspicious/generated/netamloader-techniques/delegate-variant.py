import clr
from System import MulticastDelegate
from System.Reflection import BindingFlags

def replace_callback(callback, replacement):
    slot = clr.GetClrType(MulticastDelegate).GetField("_invocationList", BindingFlags.NonPublic | BindingFlags.Instance)
    values = slot.GetValue(callback)
    values[1] = replacement
    slot.SetValue(callback, values)
