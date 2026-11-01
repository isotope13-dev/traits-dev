git_cmd = %(git -C "repo" ls-files)
files = `#{git_cmd}`
