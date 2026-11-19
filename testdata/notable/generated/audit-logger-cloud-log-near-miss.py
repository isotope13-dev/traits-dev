"""Deploy audit logger that writes to Cloud Logging."""
import os

from google.cloud import logging as cloud_logging
from google.oauth2 import service_account

_CREDS_PATH = os.environ.get("AUDIT_SA_FILE", "/etc/audit/sa.json")
_creds = service_account.Credentials.from_service_account_file(_CREDS_PATH)
_client = cloud_logging.Client(project="acme-prod", credentials=_creds)
_logger = _client.logger("audit")


def record_deploy(version: str) -> None:
    _logger.log_struct({"event": "deploy", "version": version}, severity="INFO")
