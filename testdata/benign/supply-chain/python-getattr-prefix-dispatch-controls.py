"""Framework dispatch shape: class resolved by naming-convention prefix.

Mirrors transformers' pt_to_tf.py: the TensorFlow class is resolved from the
architecture name with a visible "TF" prefix. A literal prefix joined to a
variable names the prefix honestly; only literal-plus-literal assembly hides
an API name from grep and the symbol scan.
"""
from importlib import import_module


def resolve_tf_class(architectures):
    return getattr(import_module("transformers"), "TF" + architectures[0])
