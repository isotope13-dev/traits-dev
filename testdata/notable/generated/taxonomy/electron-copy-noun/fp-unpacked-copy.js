// Redirect paths inside `x/app.asar/y` to the unpacked copy next to it.
const ARCHIVE = /([\\/])app\.asar([\\/])/;
export function outsideArchive(file) {
  return file.replace(ARCHIVE, "$1app.asar.unpacked$2");
}
