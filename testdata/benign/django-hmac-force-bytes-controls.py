import hashlib
import hmac

from django.utils.encoding import force_bytes


def make_hash(settings, sql, params):
    # Mirrors django-debug-toolbar's SQLSelectForm.make_hash: Django's
    # force_bytes helper (not the bytes() builtin) converts values for HMAC.
    m = hmac.new(key=force_bytes(settings.SECRET_KEY), digestmod=hashlib.sha1)
    for item in [sql, params]:
        m.update(force_bytes(item))
    return m.hexdigest()
