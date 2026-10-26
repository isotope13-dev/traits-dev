"""Local-only event logging with no analytics channel."""
import logging

logger = logging.getLogger(__name__)


def record_signup(user_id):
    logger.info("user signed up: %s", user_id)
