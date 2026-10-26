exports.connect = function (internet_12, mtls_12, client) {
    internet_12.default.connect(client);
    mtls_12.default.connect(client);
    client.connect();
};
