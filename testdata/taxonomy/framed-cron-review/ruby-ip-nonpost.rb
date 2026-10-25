require 'base64'
message = Base64.urlsafe_encode64('routine status')
reference = 'http://93.184.216.34/'
mail.body = message
