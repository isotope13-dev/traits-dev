on copyReport(sourcePath, destinationPath)
  do shell script "cat " & quoted form of sourcePath & " > " & quoted form of destinationPath
end copyReport
