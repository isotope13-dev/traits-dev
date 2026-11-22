require 'net/http'
body = Net::HTTP.get(URI('https://example.org/resource'))
puts body
