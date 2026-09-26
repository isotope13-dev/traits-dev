# Static matcher control only. Documentation example, never executed.

# Local kind-cluster development maps the cluster's *.svc names to loopback
# so local tools can reach in-cluster services. These entries *enable*
# access to local test doubles; they do not block any public domain.

Setup port forwarding:

```shell
kubectl -n courier-system port-forward service/kourier-internal 8080:80 &
```

### Adding localhost entries to make tools usable

Add the following entries to your `/etc/hosts` file. They resolve only
inside this guide's throwaway kind cluster, which is deleted at the end of
the session, so none of these names ever leaves the developer machine.
If a name fails to resolve, re-run the port-forward step above and check
that the corresponding service is still running in its namespace.

```txt
127.0.0.1 rekor.rekor-system.svc
127.0.0.1 fulcio.fulcio-system.svc
127.0.0.1 ctlog.ctlog-system.svc
127.0.0.1 gettoken.default.svc
127.0.0.1 tuf.tuf-system.svc
```

### Setting up environment variables

Instead of passing long URLs to every flag, export short aliases up front:

```shell
export REKOR_URL=http://rekor.rekor-system.svc:8080
export FULCIO_URL=http://fulcio.fulcio-system.svc:8080
export ISSUER_URL=http://gettoken.default.svc:8080
export TUF_MIRROR=http://tuf.tuf-system.svc:8080
```

### Smoke test

Run a quick signing smoke test against the throwaway stack:

```shell
cosign initialize --mirror $TUF_MIRROR --root ./root.json
```

Tear the cluster down when finished testing. Keep this file next to the
cluster bootstrap script for reference.

```shell
kind delete cluster --name sigstore-test
```
