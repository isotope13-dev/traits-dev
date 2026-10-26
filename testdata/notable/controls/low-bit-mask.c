/* Ordinary parity calculation, with no embedded payload or execution. */
unsigned low_bit(unsigned value) {
    return value & 1;
}
