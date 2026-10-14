"""Exception plumbing documentation (no polling code here)."""


class ParentProbeError(Exception):
    """Raised when a parent entity probe fails during param resolution.

    Wraps the original exception's message with parent-entity context for
    debuggability, while preserving the parent's ``status_code`` so the child
    can be classified the same way the parent would be.
    """

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code
