// Peer-to-peer file share: relay-only for privacy, SHA-256 to verify chunks.
export async function receiveFile(signal, onDone) {
  const ice = await (await fetch("/api/turn-credentials")).json();
  const pc = new RTCPeerConnection({ iceServers: ice.iceServers, iceTransportPolicy: "relay" });
  const channel = pc.createDataChannel("file", { ordered: true });
  const chunks = [];
  let expected = null;
  channel.onmessage = async (event) => {
    if (typeof event.data === "string") {
      const meta = JSON.parse(event.data);
      if (meta.done) {
        const blob = new Blob(chunks);
        const digest = await crypto.subtle.digest("SHA-256", await blob.arrayBuffer());
        const hex = Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, "0")).join("");
        onDone(hex === expected ? blob : null);
      } else {
        expected = meta.sha256;
      }
      return;
    }
    chunks.push(event.data);
  };
  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);
  const answer = await signal(pc.localDescription);
  await pc.setRemoteDescription(answer);
  return channel;
}
