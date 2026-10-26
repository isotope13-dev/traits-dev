const relativeName = "AWS_CONTAINER_CREDENTIALS_RELATIVE_URI", host = "http://169.254.170.2";
function credentialOptions() { return { hostname: host, path: process.env[relativeName] }; }
