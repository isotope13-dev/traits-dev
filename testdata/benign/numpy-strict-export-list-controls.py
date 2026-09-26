"""Strict dtype alias table: a CamelCase __all__ export list.

Each name embeds a dimension digit *and* a bit width (``1D...Int64``), so
every token carries two isolated digit runs with no six-letter English
word -- identifier shape, not base64 fragments.
"""
from typing import Annotated

import numpy as np

from pydantic_numpy.helper.annotation import NpArrayPydanticAnnotation

NpStrict1DArrayInt64 = Annotated[
    np.ndarray[tuple[int], np.dtype[np.int64]],
    NpArrayPydanticAnnotation.factory(data_type=np.int64, dimensions=1, strict_data_typing=True),
]

NpStrict1DArrayInt32 = Annotated[
    np.ndarray[tuple[int], np.dtype[np.int32]],
    NpArrayPydanticAnnotation.factory(data_type=np.int32, dimensions=1, strict_data_typing=True),
]

NpStrict1DArrayBool = Annotated[
    np.ndarray[tuple[int], np.dtype[np.bool_]],
    NpArrayPydanticAnnotation.factory(data_type=np.bool_, dimensions=1, strict_data_typing=True),
]

__all__ = [
    "NpStrict1DArrayInt64",
    "NpStrict1DArrayInt32",
    "NpStrict1DArrayBool",
]
