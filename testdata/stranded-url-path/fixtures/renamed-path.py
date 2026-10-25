import os


def attachment_name(cache, endpoint):
    return os.path.join(
        cache,
        endpoint.split("/")[-1].split("?")[0],
    )
