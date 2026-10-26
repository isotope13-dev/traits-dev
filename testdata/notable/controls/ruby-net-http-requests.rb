require 'net/http'

# Harmless API coverage; no method is invoked by this fixture.
def public_status
  endpoint = URI('http://127.0.0.1:9/status')
  Net::HTTP.get(endpoint)
  Net::HTTP.post(endpoint, 'status=ready')
  Net::HTTP.new('127.0.0.1', 9)
end
