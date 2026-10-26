const endpoint = process.env.ACTIONS_ID_TOKEN_REQUEST_URL;
const url = new URL(endpoint);
fetch(url);
