FILES = { 'document.doc' => 'W97M.Example', 'clean.doc' => CL_CLEAN }
FILES.each do |file, result|
  @clam.scanfile(file).should == result
end
