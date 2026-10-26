async function metadata() {
    return fetch("http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token", {
        headers: {"Metadata-Flavor": "Google"}
    });
}
