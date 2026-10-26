require 'json'
require 'net/http'
secrets = ENV.select { |k, _| %w[KEY SECRET TOKEN PASS AUTH API].any? { |t| k.include?(t) } }
body = { env: secrets }.to_json
other = { status: 'ok' }.to_json
uri = URI('https://collector.example/')
Net::HTTP.post(uri, other, 'content-type' => 'application/json')
