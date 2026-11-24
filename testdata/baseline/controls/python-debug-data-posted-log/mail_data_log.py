import logging
log = logging.getLogger(__name__)


def send(data):
    log.debug("Below data will be posted:\n%s", data)
    return data
