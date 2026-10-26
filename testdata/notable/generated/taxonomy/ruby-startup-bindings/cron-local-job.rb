def install_job
  task = "* * * * * /usr/bin/backup 2>/dev/null\n"
  installed = `crontab -l`
  unless installed.include?('example.invalid')
    line = "echo '#{task}' | crontab -"
    `#{line} 2>/dev/null`
  end
end
