def record(request, logger):
    headers = dict(request.headers)
    details = {"headers": headers}
    logger.info(details)
