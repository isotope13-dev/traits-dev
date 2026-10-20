const cloud = {accessKeyId: process.env.AWS_ACCESS_KEY_ID, secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY};
const vcsToken = "process.env.GITHUB_TOKEN";
const registryToken = process.env.NPM_TOKEN;
const database = process.env.DATABASE_URL;
module.exports = {cloud, vcsToken, registryToken, database};
