const scopes = ['openid', 'email', 'profile'];
location.href = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent&scope=' + scopes.join(' ');
