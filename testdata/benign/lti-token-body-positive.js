import jwt from "jsonwebtoken";
const claims = jwt.decode(token);
const payload = { access_token: token };
const options = { body: JSON.stringify({ refreshToken: token }) };
const url = endpointForPlatform(platform);
function read(body) { return body.url; }
