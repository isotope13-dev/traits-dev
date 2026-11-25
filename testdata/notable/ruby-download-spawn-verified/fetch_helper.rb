require 'net/http'
require 'openssl'

module FetchHelper
  def self.fetch_and_run(dest)
    uri = URI('https://downloads.example.net/releases/tool.exe')
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_PEER
    response = http.request(Net::HTTP::Get.new(uri))
    File.binwrite(dest, response.body)
    pid = Process.spawn(dest)
    Process.detach(pid)
  end
end
