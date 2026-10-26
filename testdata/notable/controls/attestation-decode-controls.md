# Static matcher control only. Documentation example, never executed.

# Inspecting a signed attestation by decoding its payload to the terminal
# for a human to read. The pipeline ends at the decoder: nothing executes
# and nothing is written, so this is inspection, not staging.

Set up short endpoint aliases first:

```shell
export TUF_MIRROR=http://tuf.tuf-system.svc:8080
export REKOR_URL=http://rekor.rekor-system.svc:8080
```

Fetch the trust root:

```shell
kubectl -n tuf-system get secrets tuf-root -ojsonpath='{.data.root}' | base64 -d > ./root.json
```

Initialize the client against the local mirror:

```shell
cosign initialize --mirror $TUF_MIRROR --root ./root.json
```

Inspect the `payload` of the attestation by base64 decoding it:

```shell
echo 'eyJfdHlwZSI6Imh0dHBzOi8vaW4tdG90by5pby9TdGF0ZW1lbnQvdjAuMSIsInN1YmplY3QiOiJkZW1vIn0' | base64 -d
```

The decoded JSON above names the demo subject. Compare it against the
digest recorded in the transparency log entry before trusting the image:

```shell
rekor-cli get --log-index 0 --format json
```

### Signing the demo image

Sign with the throwaway key, then verify the signature offline:

```shell
cosign sign --yes --key ./demo.key --tlog-upload=false registry.local:5000/sigstore/demo
cosign verify --key ./demo.pub --allow-insecure-registry registry.local:5000/sigstore/demo
```

### Attesting and checking the predicate

Attach a predicate and confirm the transparency entry exists:

```shell
cosign attest --yes --key ./demo.key --predicate ./predicate.json --tlog-upload=false registry.local:5000/sigstore/demo
cosign verify-attestation --key ./demo.pub --allow-insecure-registry registry.local:5000/sigstore/demo
```

Clean up the throwaway cluster when finished:

```shell
kind delete cluster --name sigstore-test
```
