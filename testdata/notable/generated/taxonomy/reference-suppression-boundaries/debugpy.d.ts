interface AuthFields {
  access_token: string;
  "encrypted_key": string;
}
declare class RTCPeerConnection {
  createDataChannel(label: string): RTCDataChannel;
  createOffer(): Promise<string>;
}
interface RTCDataChannel { label: string }
interface RTCIceServer { urls: string }
