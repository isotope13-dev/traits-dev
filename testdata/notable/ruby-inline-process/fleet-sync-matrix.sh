#!/bin/sh
ruby -ryaml -rjson -e '
  data = YAML.safe_load(File.read("release/fleet/repos.yml"), permitted_classes: [], aliases: false)
  repos = data.fetch("repos")
  selected = ENV.fetch("SELECTED_REPO", "")
  repos = repos.select { |repo| repo == selected } unless selected.empty?
  abort("unknown fleet repo: #{selected}") if repos.empty? && !selected.empty?
  matrix = {
    include: repos.map do |repo|
      system(
        "ruby", "fleet/sync.rb",
        "--hub-root", "release",
        "--repo-name", repo,
        "--publish",
        "--main-ref", ENV.fetch("MAIN_SHA"),
        "--validate-only"
      ) ||
        abort("invalid fleet config: #{repo}")
      { repo: repo }
    end
  }
  File.open(ENV.fetch("GITHUB_OUTPUT"), "a") { |file| file.puts("matrix=#{JSON.generate(matrix)}") }
'
