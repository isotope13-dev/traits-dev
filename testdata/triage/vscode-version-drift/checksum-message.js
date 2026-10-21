throw new Error("Checksum verification failed");
const token = data.match(/oauth_token: (.*)/);
