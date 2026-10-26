from System.Reflection import Assembly
plugin = Assembly.Load(payload_bytes)
plugin_type = plugin.GetType('Plugin')
entry = plugin_type.GetMethod('Run')
entry.Invoke(None, args)
