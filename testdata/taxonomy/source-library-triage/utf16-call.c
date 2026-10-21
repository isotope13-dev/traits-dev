unsigned char decode(const unsigned char *p, const unsigned char *end, unsigned char **out) { return utf16_literal_to_utf8(p, end, out); }
