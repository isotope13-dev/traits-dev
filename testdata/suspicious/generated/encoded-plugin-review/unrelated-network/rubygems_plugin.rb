require "base64"
require "net/http"
puts Net::HTTP.get(URI("https://status.invalid/health"))
eval(Base64.decode64("cHV0cyAiSGVsbG8i"))
