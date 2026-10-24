plugin = service.Load(payload_bytes)
entry = plugin.GetType('Plugin').GetMethod('Run')
entry.Invoke(None, args)
