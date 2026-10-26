$Stage = "C:\dist\client"
# Needed by the code-signing pipeline, which re-links the bundle
# from pre-built artifacts without rebuilding project references.
Copy-Item "$BinaryCache\installer\Release\installer.exe" $Stage
