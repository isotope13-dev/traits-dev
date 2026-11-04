target = 'preferences.conf'
contents = File.read(target)
File.write(target, contents.gsub('old', 'new'))
