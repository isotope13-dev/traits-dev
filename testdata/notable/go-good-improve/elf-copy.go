package builder
func header(out []byte) { copy(out, []byte("\x7fELF")) }
