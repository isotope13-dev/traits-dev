import android.media.MediaMuxer;
class AudioMux {
  int attach(MediaMuxer mux, android.media.MediaFormat format) {
    return mux.addTrack(format);
  }
}
