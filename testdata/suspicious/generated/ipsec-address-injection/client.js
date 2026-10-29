const endpoint = "/api/v1/network/ipsec";
const data = {tunnelModeTable: {localVpnIp: "192.168.8.9; hostname; #"}};
fetch(endpoint, {method: "PUT", body: JSON.stringify({data})});
