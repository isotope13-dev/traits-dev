$filter = Set-WmiInstance -Namespace 'root\subscription' -Class '__EventFilter' -Arguments @{Name='ProcessMonitor';QueryLanguage='WQL';Query='SELECT * FROM Win32_ProcessStartTrace'}
$consumer = Set-WmiInstance -Namespace 'root\subscription' -Class 'CommandLineEventConsumer' -Arguments @{Name='ProcessMonitor';CommandLineTemplate='eventcreate.exe /T INFORMATION /ID 100 /L APPLICATION /D Process-started'}
Set-WmiInstance -Namespace 'root\subscription' -Class '__FilterToConsumerBinding' -Arguments @{Filter=$filter;Consumer=$consumer}
