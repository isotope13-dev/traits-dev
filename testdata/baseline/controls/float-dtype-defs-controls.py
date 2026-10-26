"""Storage dtype surface: standardised floating-point dtype constructors.

The OCP microscaling float8 names (E4M3/E5M2 with FN/FNUZ suffixes) mix
letters and digits the way a renamer does, but they are industry-standard
dtype vocabulary (torch, numpy, ml_dtypes), not obfuscation. Defined once
per storage class, like torch/storage.py.
"""


class FloatStorage:
    def float8_e4m3fn(self):
        return "e4m3fn"

    def float8_e5m2fn(self):
        return "e5m2fn"

    def float8_e4m3fnuz(self):
        return "e4m3fnuz"

    def float8_e5m2fnuz(self):
        return "e5m2fnuz"


class DoubleStorage:
    def float8_e4m3fnuz(self):
        return "e4m3fnuz"

    def float8_e5m2fnuz(self):
        return "e5m2fnuz"

    def describe_dtype(self, dtype_name):
        return "dtype:" + dtype_name
