function parseFields(payload) {
    return [payload.indexOf("\x40\x03\x06"),
            payload.indexOf("\x40\x0c\x04"),
            payload.indexOf("\x05\x01\x0c\x06\x40")];
}
