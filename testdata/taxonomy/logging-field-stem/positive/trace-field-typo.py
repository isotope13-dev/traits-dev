"""Cloud Logging formatter with a typo'd trace field name."""

import logging


def make_fields(project_id, trace_id):
    return {
        "logging.googleapi.com/trace": f"projects/{project_id}/traces/{trace_id}",
    }
