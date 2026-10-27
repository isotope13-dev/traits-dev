import org.webrtc.PeerConnection;
import org.webrtc.ScreenCapturerAndroid;
import org.webrtc.VideoTrack;
class ScreenShare {
  String endpoint = "wss://example.invalid/rtc";
  void share(PeerConnection peerConnection, VideoTrack videoTrack) {
    ScreenCapturerAndroid source;
    peerConnection.addTrack(videoTrack);
  }
}
