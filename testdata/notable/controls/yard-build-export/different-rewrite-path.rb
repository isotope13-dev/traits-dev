contents = File.read('input.txt')
File.write('output.txt', contents.gsub('old', 'new'))
