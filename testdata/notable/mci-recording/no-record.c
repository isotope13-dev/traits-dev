int main(void) {
  mciSendStringA("open new Type waveaudio Alias recsound", 0, 0, 0);
  mciSendStringA("status recsound channels", 0, 0, 0);
}
