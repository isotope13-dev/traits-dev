package builder
func header() []byte {
    out := make([]byte, 64)
    out[1] = 'E'
    out[2] = 'L'
    out[3] = 'F'
    return out
}
