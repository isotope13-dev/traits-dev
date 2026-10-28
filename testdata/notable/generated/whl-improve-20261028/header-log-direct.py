def record(request, logger):
    logger.info(dict(request.headers))
