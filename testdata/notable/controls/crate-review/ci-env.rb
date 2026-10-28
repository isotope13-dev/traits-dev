runner = ENV['RUNNER_NAME']
token = ENV['GITHUB_TOKEN']
gem_key = ENV['RUBYGEMS_API_KEY']
warn runner if token && gem_key
