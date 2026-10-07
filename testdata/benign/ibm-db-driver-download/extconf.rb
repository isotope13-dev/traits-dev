#!/usr/bin/env ruby
# +----------------------------------------------------------------------+
# |  Licensed Materials - Property of IBM                                |
# |                                                                      |
# | (C) Copyright IBM Corporation 2006 - 2015                            |
# +----------------------------------------------------------------------+
require 'net/http'

DOWNLOADLINK = "http://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/linuxx64_odbc_cli.tar.gz"

def downloadCLIPackage(destination)
  uri = URI.parse(DOWNLOADLINK)
  filename = "#{destination}/clidriver.tar.gz"
  request = Net::HTTP::Get.new(uri.request_uri)
  http = Net::HTTP.new(uri.host, uri.port)
  response = http.request(request)
  f = open(filename, 'wb')
  f.write(response.body)
  f.close()
  filename
end
