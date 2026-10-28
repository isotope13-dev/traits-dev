require 'yaml'
cached = Marshal.load(Marshal.dump({name: 'cache'}))
config = YAML.load("name: cache\n")
warn cached[:name] if config['name']
