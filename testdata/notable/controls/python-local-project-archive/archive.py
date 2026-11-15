import zipfile
def archive_project(source, dest):
 with zipfile.ZipFile(dest,"w",zipfile.ZIP_DEFLATED) as archive:
  archive.write(source)
