require 'net/http'
request = Net::HTTP::Get.new('/resource')
puts request.path
