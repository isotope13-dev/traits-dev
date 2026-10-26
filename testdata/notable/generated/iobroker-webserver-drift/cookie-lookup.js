function authenticate(req) {
 const cookies = req.headers.cookie.split(';').map(c => c.trim().split('='));
 return cookies.find(c => c[0] === 'access_token');
}
