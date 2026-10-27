require 'net/http'
require 'socket'
host = Socket.gethostname
Net::HTTP.post(uri, 'status=ready')
