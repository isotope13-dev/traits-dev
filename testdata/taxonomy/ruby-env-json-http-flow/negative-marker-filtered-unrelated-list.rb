require 'json'
require 'net/http'
def transmit
  selected = ENV.select { |key, _| %w[DEBUG TRACE INFO].any? { |marker| key.include?(marker) } }
  body = { env: selected }.to_json
  uri = URI('https://collector.example/')
  Net::HTTP.post(uri, body)
end
