# AWS SDK wheel S3 context controls

The `.whl` files are tiny synthetic archives. Each declares either `boto3` or
`botocore` in wheel metadata and includes that package's `__init__.py`. The
cross-member cases put inert collector source in `addon/collector.py`; the
same-member controls put it in the SDK package member. SDK-only negatives have
no collector.

The collector uses local stub methods and fixed response data. Nothing in the
fixture is executed, and it contains no credential lookup or network call. The
`crt.sh` URL in the paired case is only a static string for taxonomy matching.

Run the focused matrix from the repository root:

```sh
python3 scripts/check-taxonomy-cases.py \
  --cleave ../cleave/target/release/cleave \
  --cases testdata/taxonomy/aws-sdk-wheel-s3-context/cases.json
```

The cases assert that outer-wheel identity remains detectable, SDK-package
operations do not become reconnaissance, add-on S3 operations remain visible
for both SDK distributions, and the certificate-transparency plus S3 pairing
still emits external-cloud surface mapping.
