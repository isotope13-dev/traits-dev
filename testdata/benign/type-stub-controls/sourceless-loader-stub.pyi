"""Type-stub declaration of the sourceless loader interface (typeshed shape).

Stubs declare; they never execute. Matching executable-loader behavior here
is a false positive, as seen with ruff's vendored
_frozen_importlib_external.pyi."""
import importlib.abc
from types import CodeType


class SourcelessFileLoader(importlib.abc.FileLoader):
    """Loader which handles sourceless file imports."""

    def get_code(self, fullname: str) -> CodeType | None: ...
    def exec_module(self, module: object) -> None: ...
