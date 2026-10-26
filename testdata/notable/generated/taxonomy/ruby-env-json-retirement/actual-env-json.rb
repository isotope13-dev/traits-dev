require "json"
value = ENV["TOKEN"]
JSON.generate({token: value})
