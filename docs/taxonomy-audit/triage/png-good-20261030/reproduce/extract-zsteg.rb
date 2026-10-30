require 'json'
require 'fileutils'
require 'zsteg'
require 'zsteg/cli/cli'

work='/tmp/png-good-triage/zsteg'
FileUtils.mkdir_p(work+'/extracted')
decoder=ZSteg::CLI::Cli.allocate
rows=JSON.parse(File.read(work+'/selected.json'))
results=File.exist?(work+'/extracted.json') ? JSON.parse(File.read(work+'/extracted.json')) : []
existing=results.map{|r|[r['index'],r['method'],r['result']]}.to_set
rows.reject!{|r|existing.include?([r['index'],r['method'],r['result']])}
rows.group_by{|r|r['index']}.each do |index, group|
  image=ZPNG::Image.load(group.first['path'],verbose: -2)
  extractor=ZSteg::Extractor.new(image, verbose: -2)
  group.each_with_index do |row,i|
    begin
      method=row['method']
      limit=row['result'].match?(/wbStego|OpenStego|Camouflage|zlib:/) ? 0 : 4096
      data=case method
      when /\Achunk:(\d+)/ then image.chunks[$1.to_i].data
      when 'imagedata' then image.imagedata
      when /\Ameta / then nil
      else extractor.extract(decoder.decode_param_string(method).merge(limit:limit))
      end
      next unless data
      dest="#{work}/extracted/#{'%03d'%index}-#{'%03d'%i}.bin"
      File.binwrite(dest,data)
      results << row.merge('extracted_path'=>dest,'size'=>data.bytesize,'extraction_limit'=>limit)
    rescue => e
      results << row.merge('error'=>e.to_s)
    end
  end
  File.write(work+'/extracted.json',JSON.pretty_generate(results)+"\n")
  puts "#{index}: extracted #{group.size} candidates"
  STDOUT.flush
end
