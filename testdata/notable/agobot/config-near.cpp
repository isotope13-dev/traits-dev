void Config() {
 g_cMainCtrl.m_cIRC.m_vServers.push_back(&server);
 SetCvar(&bot_seclogin, enabled);
 SetCvar(&as_service, enabled);
 // SetCvar(&bot_meltserver, enabled);
}
