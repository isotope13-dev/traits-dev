int main(void) {
  mciSendStringA("open new Type waveaudio Alias recsound", 0, 0, 0);
  mciSendStringA("RECORD recsound", 0, 0, 0);
  mciSendStringA("SAVE recsound recording.wav", 0, 0, 0);
}
