#include <stdint.h>
#include <string.h>
#define STATE_BITS 288
#define KEY_BYTES 10
#define IV_BYTES 10
static uint8_t next_bit(uint8_t registers[STATE_BITS]) {
  uint8_t t1 = registers[ 65 ] ^ registers[ 92 ];
  uint8_t t2 = registers[ 161 ] ^ registers[ 176 ];
  uint8_t t3 = registers[ 242 ] ^ registers[ 287 ];
  uint8_t output = t1 ^ t2 ^ t3;

  t1 ^= (registers[ 90 ] & registers[ 91 ] ) ^ registers[ 170 ];
  t2 ^= (registers[ 174 ] & registers[ 175 ] ) ^ registers[ 263 ];
  t3 ^= (registers[ 285 ] & registers[ 286 ] ) ^ registers[ 68 ];

  for (int i = 92; i > 0; i--) registers[i] = registers[i - 1];
  registers[ 0 ] = t3;

  for (int i = 176; i > 93; i--) registers[i] = registers[i - 1];
  registers[ 93 ] = t1;

  for (int i = 287; i > 177; i--) registers[i] = registers[i - 1];
  registers[ 177 ] = t2;

  return output;
}

static void transform(uint8_t *data, size_t length,
  const uint8_t key[KEY_BYTES],
  const uint8_t iv[IV_BYTES]) {
  uint8_t registers[STATE_BITS] = {0};

  for (int i = 0; i < 80; i++) {
    registers[i] = (key[9 - i / 8] >> (7 - i % 8)) & 1;
    registers[i + 93] = (iv[9 - i / 8] >> (7 - i % 8)) & 1;
  }
  registers[ 285 ] = 1;
  registers[ 286 ] = 1;
  registers[ 287 ] = 1;

  for (int i = 0; i < 4 * STATE_BITS; i++) next_bit(registers);

  for (size_t i = 0; i < length; i++) {
    uint8_t stream_byte = 0;
    for (int bit = 0; bit < 8; bit++)
      stream_byte |= next_bit(registers) << bit;
    data[i] ^= stream_byte;
  }
}

static int check_test_vector(void) {
  const uint8_t key[KEY_BYTES] = {0x80};
  const uint8_t iv[IV_BYTES] = {0};
  const uint8_t expected[ 16 ] = {
    0x38, 0xeb, 0x86, 0xff, 0x73, 0x0d, 0x7a, 0x9c,
    0xaf, 0x8d, 0xf1, 0x3a, 0x44, 0x20, 0x54, 0x0d
  };
  uint8_t output[sizeof(expected)] = {0};

  transform(output, sizeof(output), key, iv);
  return memcmp(output, expected, sizeof(expected)) == 0;
}

