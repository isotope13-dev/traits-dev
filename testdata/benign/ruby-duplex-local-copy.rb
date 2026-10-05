pipe = IO.popen(['/bin/sh'], 'r+')
Thread.new { IO.copy_stream(STDIN, pipe) }
IO.copy_stream(pipe, STDOUT)
