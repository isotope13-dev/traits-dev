// Connected session client without any host inventory: login, heartbeat,
// and WebSocket session handling only. No hardware identifiers are read, so
// fingerprint composites must stay silent and notable stays the ceiling.
import axios from 'axios';
import WebSocket from 'ws';

export class SessionClient {
  constructor(baseURL) {
    this.api = axios.create({baseURL, timeout: 30000});
    this.sessionId = null;
    this.token = null;
    this.ws = null;
    this.timer = null;
  }

  async signIn(username, password) {
    const res = await this.api.post('/auth/login', {username, password});
    this.token = res.data.access_token;
    this.sessionId = res.data.session_id;
    return res.data;
  }

  async heartbeat() {
    const res = await this.api.post('/session/heartbeat', {}, {
      headers: {'X-Session-ID': this.sessionId}
    });
    return res.data;
  }

  startPulse(seconds = 15) {
    this.timer = setInterval(() => {
      this.heartbeat().catch(() => {});
    }, seconds * 1000);
  }

  stopPulse() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  linkSocket(url) {
    this.ws = new WebSocket(url);
    this.ws.on('open', () => {
      this.ws.send(JSON.stringify({type: 'hello', session_id: this.sessionId}));
    });
  }
}
