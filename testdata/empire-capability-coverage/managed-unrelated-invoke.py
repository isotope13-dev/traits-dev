from System.Reflection import Assembly
plugin = Assembly.Load(payload_bytes)
entry = plugin.GetType('Plugin').GetMethod('Run')
unrelated.Invoke(None, args)
