class ToolboxError(Exception):
    """Base class for exceptions in this module."""

    ...


class CacheFailureError(ToolboxError):
    """Exception raised when a cache lookup fails."""

    ...
