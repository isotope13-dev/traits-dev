"""CIS benchmark check module shape (benign scanner control).

Mirrors a compliance collector: list buckets, read each bucket's
public-access posture, report findings. Runs as the product's audit job.
"""
from agent_bom.security import sanitize_text


def check_s3_public_access(s3_client):
    findings = []
    buckets = s3_client.list_buckets().get("Buckets", [])
    for bucket in buckets:
        name = bucket["Name"]
        block = s3_client.get_public_access_block(Bucket=name).get(
            "PublicAccessBlockConfiguration", {}
        )
        status = s3_client.get_bucket_policy_status(Bucket=name).get(
            "PolicyStatus", {}
        )
        findings.append({
            "bucket": sanitize_text(name),
            "blocked": bool(block),
            "public": bool(status.get("IsPublic")),
        })
    return findings
