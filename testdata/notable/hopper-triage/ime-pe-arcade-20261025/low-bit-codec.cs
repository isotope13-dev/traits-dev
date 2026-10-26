// Bitstream arithmetic without staged-code activation is a neutral capability.
class Codec {
 int Decode(int value, int bit) { return (value << 1) | (bit & 1); }
}
