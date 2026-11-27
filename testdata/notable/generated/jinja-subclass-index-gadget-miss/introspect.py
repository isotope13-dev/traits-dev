#!/usr/bin/env python3
# Lists loaded exception classes for a debug report. No template syntax.
def loaded_exceptions() -> list:
    base = BaseException
    names = [cls.__name__ for cls in base.__subclasses__()]
    return sorted(names)[:3]
