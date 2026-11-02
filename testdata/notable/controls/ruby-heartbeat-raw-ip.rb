require 'net/http'
req = Net::HTTP::Post.new(URI("http://45.9.1.2/c"))
req.body = "heartbeat"
