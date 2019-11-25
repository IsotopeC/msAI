
"""msAI exception hierarchy.

"""


import logging


logger = logging.getLogger(__name__)
"""Module logger."""


class msAIerror(Exception):
    """Base class for exceptions in the msAI package."""

    pass


class RootError(msAIerror):
    """Exceptions raised for errors in msAI package __init__."""

    message: str
    """Explanation of the cause of this error."""

    def __init__(self, message: str):
        """Initializes an instance of RootError.

        Args:
            message: Explanation of the cause of this error.
        """

        self.message: str = message


class MiscUtilsError(msAIerror):
    """Exceptions raised for errors in miscUtils the module."""

    def __init__(self, message):
        """Initializes an instance of MiscUtilsError.

        Args:
            message: Explanation of the cause of this error.
        """

        self.message = message


class MetadataError(msAIerror):
    """Exceptions raised for errors in the metadata module."""

    def __init__(self, message):
        self.message = message


class MetadataInitError(MetadataError):
    """Exceptions raised for errors in initializing metadata."""

    def __init__(self, message):
        self.message = message


class MetadataVerifyError(MetadataError):
    """Exceptions raised for errors in verifying imported metadata."""

    def __init__(self, message):
        self.message = message


class MetadataIndexError(MetadataError):
    """Exceptions raised for errors in setting metadata index."""

    def __init__(self, message):
        self.message = message


class SampleRunError(msAIerror):
    """Exceptions raised for errors in the SampleRun module."""

    def __init__(self, message):
        self.message = message


class SampleRunMSinitError(SampleRunError):
    """Exceptions raised for errors in initializing MS data in SampleRun."""

    def __init__(self, message):
        self.message = message


class MSdataError(msAIerror):
    """Exceptions raised for errors in the msData module."""

    def __init__(self, message):
        self.message = message


class MSfileSetInitError(MSdataError):
    """Exceptions raised for errors in initializing MSfileSet."""

    def __init__(self, message):
        self.message = message
