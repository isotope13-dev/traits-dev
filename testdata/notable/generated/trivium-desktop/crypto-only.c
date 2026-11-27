/*
 * hack.c - Trivium payload encryption and decryption
 * author: @cocomelonc
 * https://cocomelonc.github.io/malware/2026/11/27/malware-cryptography-47.html
 */

#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define STATE_BITS 288
#define KEY_BYTES 10
#define IV_BYTES 10

static const uint8_t payload[] = "hello cipher";

static uint8_t trivium_clock(uint8_t state[STATE_BITS]) {
  uint8_t t1 = state[65] ^ state[92];
  uint8_t t2 = state[161] ^ state[176];
  uint8_t t3 = state[242] ^ state[287];
  uint8_t output = t1 ^ t2 ^ t3;

  t1 ^= (state[90] & state[91]) ^ state[170];
  t2 ^= (state[174] & state[175]) ^ state[263];
  t3 ^= (state[285] & state[286]) ^ state[68];

  for (int i = 92; i > 0; i--) state[i] = state[i - 1];
  state[0] = t3;

  for (int i = 176; i > 93; i--) state[i] = state[i - 1];
  state[93] = t1;

  for (int i = 287; i > 177; i--) state[i] = state[i - 1];
  state[177] = t2;

  return output;
}

static void trivium_crypt(uint8_t *data, size_t length,
  const uint8_t key[KEY_BYTES],
  const uint8_t iv[IV_BYTES]) {
  uint8_t state[STATE_BITS] = {0};

  for (int i = 0; i < 80; i++) {
    state[i] = (key[9 - i / 8] >> (7 - i % 8)) & 1;
    state[i + 93] = (iv[9 - i / 8] >> (7 - i % 8)) & 1;
  }
  state[285] = 1;
  state[286] = 1;
  state[287] = 1;

  for (int i = 0; i < 4 * STATE_BITS; i++) trivium_clock(state);

  for (size_t i = 0; i < length; i++) {
    uint8_t stream_byte = 0;
    for (int bit = 0; bit < 8; bit++)
      stream_byte |= trivium_clock(state) << bit;
    data[i] ^= stream_byte;
  }
}

static int check_test_vector(void) {
  const uint8_t key[KEY_BYTES] = {0x80};
  const uint8_t iv[IV_BYTES] = {0};
  const uint8_t expected[16] = {
    0x38, 0xeb, 0x86, 0xff, 0x73, 0x0d, 0x7a, 0x9c,
    0xaf, 0x8d, 0xf1, 0x3a, 0x44, 0x20, 0x54, 0x0d
  };
  uint8_t output[sizeof(expected)] = {0};

  trivium_crypt(output, sizeof(output), key, iv);
  return memcmp(output, expected, sizeof(expected)) == 0;
}

static void print_hex(const char *label, const uint8_t *data, size_t length) {
  printf("%s", label);
  for (size_t i = 0; i < length; i++) {
    printf("%02x", data[i]);
    if ((i + 1) % 16 == 0 || i + 1 == length) printf("\n");
    else printf(" ");
  }
}

int main(void) {
  static const uint8_t key[KEY_BYTES] = {
    0x10, 0x32, 0x54, 0x76, 0x98, 0xba, 0xdc, 0xfe, 0x01, 0x23
  };
  static const uint8_t iv[IV_BYTES] = {
    0xa0, 0x91, 0x82, 0x73, 0x64, 0x55, 0x46, 0x37, 0x28, 0x19
  };

  if (!check_test_vector()) {
    fprintf(stderr, "Trivium test vector failed\n");
    return 1;
  }
  puts("Trivium eSTREAM test vector: OK");

  const size_t payload_length = sizeof(payload) - 1;
  uint8_t encrypted[sizeof(payload) - 1];
  uint8_t decrypted[sizeof(payload) - 1];

  memcpy(encrypted, payload, payload_length);
  trivium_crypt(encrypted, payload_length, key, iv);
  print_hex("encrypted payload: ", encrypted, payload_length);

  memcpy(decrypted, encrypted, payload_length);
  trivium_crypt(decrypted, payload_length, key, iv);
  if (memcmp(decrypted, payload, payload_length) != 0) {
    fprintf(stderr, "payload decryption failed\n");
    return 1;
  }

  print_hex("decrypted payload: ", decrypted, payload_length);
  printf("payload decryption: OK (%zu bytes)\n", payload_length);

  puts("linux demo checks encryption and decryption, meow =^..^=!");

  return 0;
}
