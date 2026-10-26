const relativeName = "AWS_CONTAINER_CREDENTIALS_RELATIVE_URI", host = "http://127.0.0.1";
function credentialOptions() { return { hostname: host, path: process.env[relativeName] }; }
