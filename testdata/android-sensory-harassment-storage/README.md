# Fixtures for android-sensory-harassment-storage

Built from the Java sources in `src/` with only javac and d8 (Android
stubs stand in for framework classes, so no SDK is needed):

  javac --release 8 -d out <stubs> <Main>.java
  d8 --min-api 26 --output out.zip <classes>

- `wallpaper-torch-storage.dex`: sets wallpaper via `setResource` and
  touches torch plus external storage (positive).
- `torch-storage-no-wallpaper.dex`: torch plus storage only, mirroring a
  camera library bundled with file access (negative: the wallpaper leg
  must carry the conviction).
