const args = process.argv.slice(2);
const username = process.env.CAAS_ARTIFACTORY_READER_USERNAME || '';
const password = process.env.CAAS_ARTIFACTORY_READER_PASSWORD || '';
const target = 'https://packages.example.com/artifactory/api/go/golang-main/@v/list';
console.log(args.length, username.length, password.length, target);
