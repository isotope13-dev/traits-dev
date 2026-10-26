require 'net/http'
Net::HTTP.start('127.0.0.1', 80) { |http| http.request(request) }
