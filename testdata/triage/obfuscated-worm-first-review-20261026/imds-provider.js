function za() {
    return {
        label: "instance-metadata",
        resolve: async () => {
            let t = await fetch("http://169.254.169.254/latest/api/token", {
                method: "PUT",
                headers: {
                    "X-aws-ec2-metadata-token-ttl-seconds": "21600"
                },
                signal: AbortSignal.timeout(2000)
            });
            if (!t.ok) throw Error(`IMDS token ${t.status}`);
            let n = {
                    "X-aws-ec2-metadata-token": await t.text()
                },
                s = await fetch("http://169.254.169.254/latest/meta-data/iam/security-credentials/", {
                    headers: n,
                    signal: AbortSignal.timeout(2000)
                });
            if (!s.ok) throw Error(`IMDS role ${s.status}`);
            let i = (await s.text()).trim().split(`
`)[0],
                o = await fetch(`http://169.254.169.254/latest/meta-data/iam/security-credentials/${i}`, {
                    headers: n,
                    signal: AbortSignal.timeout(2000)
                });
            if (!o.ok) throw Error(`IMDS creds ${o.status}`);
            let a = await o.json();
            return {
                accessKeyId: a.AccessKeyId,
                secretAccessKey: a.SecretAccessKey,
                sessionToken: a.Token
            }
        }
    }
}
