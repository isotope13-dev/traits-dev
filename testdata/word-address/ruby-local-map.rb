table = {"maple" => 192, "cedar" => 0, "birch" => 2, "oak" => 17}
words = ["maple", "cedar", "birch", "oak"]
puts words.map { |word| table.fetch(word) }.join(".")
