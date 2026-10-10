require 'base64'
encoded = Base64.strict_encode64('sample')
Base64.strict_decode64(encoded)
