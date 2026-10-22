log = File.open('application.log', 'a')
STDOUT.reopen(log)
STDERR.reopen(log)
