require "open-uri"
def field(text, start, finish)
  text.downcase.split(start)[1].split(finish)[0].strip
end
text = URI.open("https://raw.githubusercontent.com/example/status/main/notice.txt").read
puts field(text, "[title]", "[/title]")
